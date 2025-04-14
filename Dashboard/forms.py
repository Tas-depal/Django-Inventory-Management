from django import forms
from .models import Product, Order, Category,Customer

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['name','category','description','quantity','amount_per','image']

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['product','order_quantity']
		

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ['name','product','quantity']

class CategoryForm(forms.ModelForm):
	class Meta:
		model=Category
		#the fields to be displayed in the form
		fields=['name','image']