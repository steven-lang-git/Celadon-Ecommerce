from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import json
import datetime
from .forms import CouponForm, RegisterForm, UserUpdateForm, ProfileUpdateForm, ContactForm, ShippingForm, StateForm, CustomAuthenticationForm
from django.utils import timezone
from decimal import Decimal
import random





from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from django.views.generic import DetailView

from .models import *
import logging
import logging.config
import sys
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .utils import cookieCart, cartData, guestOrder
from django.core.mail import send_mail, BadHeaderError

# Create your views here.


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    category = Category.objects.all()
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')

    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.objects.order_by('name')
        # products = Product.get_all_products()

    store_paginator = Paginator(products, 4)

    page_num = request.GET.get('page')

    page = store_paginator.get_page(page_num)

    sort_order = request.GET.get('orderby')
    if sort_order == 'latest':
        products = Product.objects.order_by('-created_at')
    if sort_order== 'lowest_price':
        products = Product.objects.order_by('price')
    if sort_order== 'highest_price':
        products = Product.objects.order_by('-price')
    else:
        products = products.all()

    context = {'products': products,
               'cartItems': cartItems,
               'categories': categories,
               'category': category,
               'page': page,
               'sort_order': sort_order,


               }
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    total = Decimal(order.get_cart_total)
    if cartItems == 0:
        messages.error(request, 'Please add items to your cart to proceed.')
    else:
        messages.success(request, 'Ready for checkout')
    
 


    coupon_form = CouponForm(request.POST)

    if coupon_form.is_valid():

        coupon_code = coupon_form.cleaned_data['code']
        print(f"Received coupon code: {coupon_code}")  # Add this line to see if the code is being received

        try:
            coupon = Coupon.objects.get(
                code=coupon_code,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now(),
                active=True
            )
            if cartItems > 0:  # Check if there is at least 1 item in the cart
                total -= coupon.discount
                order.cart_total = total  # Update the cart total
                order.save()  # Save the changes to the order
            print(f"Discount applied: {coupon.discount}")  # Add this line to see if the discount is applied
            print(f"New Total: {total}")
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')
    else:
        print('Coupon form is invalid')
      
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'total':total, 'coupon_form': coupon_form}
    return render(request, 'store/cart.html', context)



def process_url_from_client(request):
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            print('form is valid')
            form.save()
    else:
        print('not post')
        form = ShippingForm()
    context = {
        "form": form,
    }


def get_user_pending_order(request):
    user_profile = get_object_or_404(Profile,user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        return order[0]
    return 0 

def order_details(request, **kwargs):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        orders = Order.objects.filter(customer=customer, complete=True)


    context = {
        'orders':orders,
        'items': items,
    }
    return render(request, 'store/order_summary.html', context)

def checkout(request):
    # zip_code = ZipCode.get("90210")
    # tax_rate = zip_code.applicable_tax_rate
    # percentage = ZipCode.tax_rate_to_percentage(tax_rate)
    # print(zip_code)
    # print(tax_rate)
    # print(percentage)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    form = StateForm(request.POST or None)
    answer = ''
    # if form.is_valid():
    #     answer = form.cleaned_data.get('state')
    #     print(answer)


    context = {'items': items, 'order': order, 'cartItems': cartItems, 'form':form, 'states':states}
    return render(request, 'store/checkout.html', context)




def updateItem(request):
    print('Request body:', request.body)

    data = json.loads(request.body)
    print('data:',data)
    productId = data['productId']
    action = data['action']
    quantity = int(data['quantity'])  # Parse the quantity as an integer

    print('quantity:', quantity)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'delete':
        try:
            orderItem.quantity = 0
        except Exception as e:
            print('Error during deletion:', str(e))
    elif action == 'increment':
        orderItem.quantity += 1
    elif action == 'decrement':
        orderItem.quantity -= 1
    elif action == 'add':
        orderItem.quantity += quantity
  

    print("newest quantity after adding",orderItem.quantity)

    if orderItem.quantity <= 0:
        orderItem.delete()
        print('this time delete happened')
    else:
        orderItem.save()


    return JsonResponse('Item was added', safe=False)


# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print(data)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order =guestOrder(request,data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
  

    return JsonResponse('Payment completed..', safe=False)


def paymentSuccess(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {'cartItems': cartItems, }
    return render(request, 'store/payment_successful.html', context=context)

def product_detail(request, id):
    product = Product.objects.get(id=id)
    category = Category.objects.all()
    # images = Images.objects.filter(product_id=id)
    # for comments can have parameter for status='True' or 'New'
    comments = Comment.objects.filter(product_id =id)


    # get all other products other than the one we are viewing
    all_products = Product.objects.exclude(id=id)

    #get 4 random products from the product list
    related_products = random.sample(list(all_products),4)


    comments_paginator = Paginator(comments,3)

    page_num = request.GET.get('page')

    page = comments_paginator.get_page(page_num)

    context={ 'product' : product,
              'category':category,
              'comments': comments,
              'page': page,
              'related_products': related_products,
              }



    return render(request, 'store/product.html', context=context)




# def category_detail(request, slug):
#     category = Category.objects.all()
#     products = Product.objects.filter(category_id=id)
#     context={'products': products,
#              'category': category}
#     return render(request,'categories.html',context)


def about(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {'cartItems': cartItems, }
    return render(request, 'store/about.html', context)


def contact(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    if request.method =='GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try: 
                send_mail(subject,message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header founder.')
            return redirect('success')

    context = {'cartItems': cartItems, 'form': form }
    return render(request, 'store/contact.html', context)

def successView(request):
    return render(request, 'store/success_contact.html')

# def search(request):
#     if request.method == 'POST':
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             query = form.cleaned_data['query'] # get form input data
#             catid = form.cleaned_data['catid']
#             if catid==0:
#                 products=Product.objects.filter(product__icontains=query) # select from product where product like '%query%'
#             else:
#                 products = Product.objects.filter(product__icontains=query,category_id=catid)
#
#             Category = Category.objects.all()
#             context={'products': products, 'query': query, 'category':category}
#
#             return render(request, 'search_products.html', context)
#         return HttpResponseRedirect('/')
#
#
#
# def get_products(request):
#     if request.is_ajax():
#         q = request.GET.get('term','')
#         products = Product.objects.filter(product_icontains=q)
#         results = []
#         for pr in products:
#             product_json = {}
#             product_json = pr.name + "," + pr.price
#             results.append(product_json)
#         data = json.dumps(results)
#     else:
#         data = 'fail'
#     mimetype = 'application/json'
#     return HttpResponse(data, mimetype)

def autocomplete(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(name__icontains=request.GET.get('term'))

        names = list()
        prod = dict()
        # for product in qs:
        #     names.append(product.name)
        #     print(product.name)

        # titles = [product.title for product in qs]
        for product in qs:
            prod["label"] = product.id
            prod["value"] = product.name
            names.append(prod.copy())
        return JsonResponse(names, safe=False)
    return render(request, 'store/main.html')


def addcomment(request,proid):
    url = request.META.get('HTTP_REFERER')
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            data=Comment() # create relation with model.
            # data.name = form.cleaned_data['name'] # get form input data
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.product_id=proid
            current_user = request.user
            # data.user_id=current_user.id
            data.user = current_user
            data.post = list
            data.ip = request.META.get('REMOTE_ADDR')
            data.save() #save data to table
            # messages.success(request,"Your message is sent. Thank you for your message.")
            return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(url)


def category(request, id):
    categories = Category.get_all_categories()
    products = Product.get_all_products_by_categoryid(id)

    category = Category.objects.all()
    categoryID = request.GET.get('category')
    category_select = Category.get_select(id)


    store_paginator = Paginator(products, 1)

    page_num = request.GET.get('page')

    page = store_paginator.get_page(page_num)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {
        'categories': categories,
        'category_select':category_select,
        'products':products,
        'page':page,
        'cartItems':cartItems,
    }


    return render(request, 'store/categories.html',context)


def home_view(request):
    return render(request, 'store/store.html')

def sign_up(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        data = Customer()
        data_2 = Profile()
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        data.user = user
        data_2.user = data.user
        data.email = form.cleaned_data.get('email')
        data.save()
        data_2.save()
        login(request, user)
        messages.success(request,f'account has been created.')
        return redirect('store')
    # else:
    #     messages.error(request,f'Please fill out the fields correctly.')
    #     form = RegisterForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def profile(request):
    if request.method =='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'account has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }    

    return render(request, 'profile.html',context)

# def view_profile(request):
#     context = {'user' : request.user}
#     return render(request, 'profile.html', context)
# #
def search(request):
    if request.method == 'GET':
        search = request.GET.get('productSearch')
        if not search:
            search = ""
        product = Product.objects.all().filter(name__icontains=search)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    return render(request, 'store/search.html', {'product':product, 'search':search, 'cartItems':cartItems})

def login_view(request):
    print("Entering login_view function")  # Print a message when the function is entered

    if request.method == "POST":
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Corrected function name
                return redirect("home")
    else:
        form = CustomAuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


