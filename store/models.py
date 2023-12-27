from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.db.models import Avg
from PIL import Image
from django.utils import timezone

CATEGORY_CHOICES = (
    ('A', 'Ambulatory'),
    ('G', 'Gloves'),
    ('O', 'Orthopedic'),
    ('R','Respiratory'),
    ('SK', 'Skin Care'),
    ('SY', 'Syringes / Needles / Infusion')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)
SHIPPING_METHODS = [('option1','Standard'),('option2','Express'),('option3','Rush')]


class Category(models.Model):
    name = models.CharField(max_length=20,default=" ")

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_select(id):
        return Category.objects.get(id=id)


    def __str__(self):
        return self.name




# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg' , upload_to='profile_pics')
    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self):
    #     super().save()
    #     img = Image.open(self.image.path)

    #     if img.height >300 or img.width >300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

class Product(models.Model):

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    # category = models.CharField(choices =CATEGORY_CHOICES, max_length=2, null = True, blank = True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, default=1)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    secondImage = models.ImageField(null=True, blank=True, upload_to='images/')
    # user field needs to allow nulls
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)




    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url= self.image.url
        except:
            url = ''
        return url

    @property
    def imageURL_2(self):
        try:
            url = self.secondImage.url
        except:
            url = ''
        return url



    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products()
    @property
    def avg_rating(self):
        sum = 0
        comments = Comment.objects.filter(product_id=self.id)
        for comment in comments:
            sum += comment.rate
        if len(comments) >0:
            return int(sum/len(comments))
        else:
            return 0

    @property
    def avg_len(self):
        comments = Comment.objects.filter(product_id=self.id)
        if len(comments)>0:
            return len(comments)
        else:
            return 0

    @property
    def testLength(self):
        comments = Comment.objects.filter(product_id=self.id)
        if len(comments) > 0:
            return len(comments)
        else:
            return 0




def slug_generator(sender,instance, *args, **kwargs):
        if not instance.slug:
            instance.slug='SLUG'


pre_save.connect(slug_generator, sender=Product)

class Order(models.Model):
    # ref_code = models.CharField(max_length=15, blank=True,null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null = True)
    shipping_methods = models.BooleanField(default=False)
    ship_window = models.BooleanField(default=False)
    service = models.CharField(
                    max_length = 20,
                    choices = SHIPPING_METHODS, # Just a list of Ground, 2day, etc
                    default = "Standard")

    def __str__(self):
        if self.id==None:
            return "ERROR-ORDER IS NULL"
        return str(self.id)
  
    def get_order_items(self):
        return OrderItem.objects.filter(order=self)

    # def __str__(self):
    #     return '{0} - {1}'.format(self.owner, self.ref_code)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    # def save(self, force_insert=False, force_update=False, using=None):
    #     self.save(force_insert, force_update, using)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_ordered= models.DateTimeField(null=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Comment(models.Model):
    STATUS =(
        ('New', 'New'),
        ('True','True'),
        ('False', 'False'),
    )

    RATING = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    )


    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=998, blank=True)
    comment = models.CharField(max_length=8000, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10, choices=STATUS, default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']



        # widget = {
        #     'subject': TextInput(attrs={'class':'input', 'placeholder': 'subject'}),
        #     'message' : Textarea(attrs={'class':'input', 'placeholder':'Your Review'}),
        #     'rating': Textarea(attrs={'class': 'input'}),
        #     }

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to

    def apply_discount(self, total):
        if self.is_valid():
            return total - (total * (self.discount / 100))
        return total

    def __str__(self):
        return self.code