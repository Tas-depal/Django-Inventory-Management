from django.db import models

#manually added
#to link tables to one another
from django.contrib.auth.models import(User)

class Category(models.Model):
	name = models.CharField(max_length=100, null=True)
	image = models.ImageField(default='avatar.png',upload_to='Category_Images')

	class Meta:
		verbose_name_plural = 'Category'

	def __str__(self):
		return f'{self.name}'

class Product(models.Model):
	name = models.CharField(max_length=100, null=True,unique=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
	quantity = models.PositiveIntegerField(null=True)
	amount_per = models.PositiveIntegerField(null=True)
	description = models.CharField(max_length=500, null=True)
	image = models.ImageField(default='avatar.png',upload_to='Product_Images')

	#to change table name fron its plural form 
	class Meta:
		verbose_name_plural = 'Product'

	def save(self, *args, **kwargs):
		self.name = self.name.lower()
		super(Product, self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.name}' 

class Order(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	staff = models.ForeignKey(User, models.CASCADE, null=True)
	order_quantity = models.PositiveIntegerField(null=True)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Order'

	def __str__(self):
		return f'{self.order_quantity}-{self.product} ordered by {self.staff.username}' 

class Customer(models.Model):
	name = models.CharField(max_length=100, null=True,unique=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	quantity = models.PositiveIntegerField(null=True)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Customer'

	def __str__(self):
		return f'{self.product} ordered by {self.name}' 

