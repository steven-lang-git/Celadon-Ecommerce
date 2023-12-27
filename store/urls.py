from django.urls import path, include
from django.contrib import admin
# from django.conf import settings
# from django.conf.urls.static import static
from . import views


from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) 
#     # urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


urlpatterns = [
    path('',views.store, name="store"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('category/<int:id>/',views.category, name="category"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_url_from_client/', views.process_url_from_client, name="process_url_from_client"),
    path('process_order/', views.processOrder, name="process_order"),
    path('products/<int:id>/', views.product_detail, name='product'),
    path('product/addcomment/<int:proid>', views.addcomment, name='addcomment'),
    path('about/', views.about, name='about'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('signup/', views.sign_up, name='signup'),
    path('admin/', admin.site.urls),
    path('search/',views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('order-summary/',views.order_details, name='order_summary'),
    path('payment_succesful/',views.paymentSuccess, name='paymentSuccessful'),
    path('contact/',views.contact, name='contact'),
    path('success/', views.successView, name='success'),
    path(
        'login/',
        LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=CustomAuthenticationForm
            ),
        name='login'
    ),

    # path('profile/edit/', views.edit_profile, name='edit_profile')
    # path('', views.home_view, name="home"),
    # path('category_detail/<int:id>/<slug:slug>', views.category_detail, name='category')
]

