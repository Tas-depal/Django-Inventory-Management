from django.contrib import admin
from .models import Product, Order, Category,Customer
from django.contrib.auth.models import(Group)

# Register your models here.

#manually added

#admin header
admin.site.site_header = 'Inventory Management'

#To display products in table form
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name','category','quantity','amount_per')
	list_filter = ['category']

class OrderAdmin(admin.ModelAdmin):
	list_display = ('product','order_quantity','staff','date')
	list_filter = ['staff']

class CustomerAdmin(admin.ModelAdmin):
	list_display = ('name','product','quantity','date')
	list_filter = ['name']

admin.site.register(Product, ProductAdmin)

admin.site.register(Order,OrderAdmin)

admin.site.register(Category)

admin.site.register(Customer,CustomerAdmin)


# to unregister groups from admin panel
# admin.site.unregister(Group)
