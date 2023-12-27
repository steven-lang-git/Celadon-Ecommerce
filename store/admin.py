from django.contrib import admin

# Register your models here.

from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User


@admin.register(Product,Category, ShippingAddress, OrderItem, Order,Customer,Profile,Coupon)
class ViewAdmin(ImportExportModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    list_display=['subject','comment','status','create_at']

admin.site.register(Comment,CommentAdmin)