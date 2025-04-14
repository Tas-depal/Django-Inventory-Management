import xlwt
from django.shortcuts import render,redirect

#manually added
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

#product, category and order table imported from database
from .models import Product, Order, Category,Customer
from .forms import ProductForm,OrderForm,CategoryForm,CustomerForm

#imported user model
from django.contrib.auth.models import User

#import Profile Model

from User.models import Profile

#messages imported
from django.contrib import messages


#manually added
#to ensure no one enters directly without logging in
@login_required
def index(request):
	#fetch order details
	order = Order.objects.all()
	order_count = order.count()

	customer = Customer.objects.all()
	customer_count = customer.count()

	staff = User.objects.all()
	staff_count = staff.count()

	if request.method=='POST':
		form =OrderForm(request.POST)
		if form.is_valid():
			#these three lines are used to send the data of staff member who orders the product
			instance = form.save(commit=False)
			instance.staff = request.user
			instance.save()
			order_id = instance.id
			order_qty = instance.order_quantity
			prodId = instance.product_id
			product_qty = list(Product.objects.filter(id=prodId).values())[0]['quantity']
			updated_qty = order_qty+product_qty
			Product.objects.filter(id=prodId).update(quantity=updated_qty)

			return redirect('dashboard-index')
	else:
		form = OrderForm()

	#fetch product details
	items = Product.objects.all()
	product_count = items.count()
	context={
		'order':order,
		'items':items,
		'form':form,
		'staff_count':staff_count,
		'order_count':order_count,
		'product_count':product_count,
		'customer':customer,
		'customer_count':customer_count,
	}
	return render(request,'dashboard/index.html',context)

@login_required
def staff(request):
	staff = User.objects.all()
	context={
		'staff':staff,
	}
	return render(request,'dashboard/staff.html',context)

@login_required
def staff_detail(request,pk):
	staff = User.objects.get(id=pk)
	context={
		'staff':staff
	}

	return render(request,'dashboard/staff_detail.html',context)

@login_required
def products(request):
    #using orm
	# items = Product.objects.raw('SELECT *, (quantity*amount_per) as total_amount FROM dashboard_product')
	items = Product.objects.all()
	if request.method=='POST':
		form = ProductForm(request.POST)
		name = request.POST['name']
		product_exists = Product.objects.filter(name=name).exists()
		if product_exists:
			messages.warning(request, 'This product already exists.')
			return redirect('dashboard-products')
		if form.is_valid():
			#to save form data to database
			form.save()
			product_name = form.cleaned_data.get('name')
			messages.warning(request,f'{product_name} has been added')

			return redirect('dashboard-products')
	else:
		form = ProductForm()
	context={
		'items' : items,
		'form':form
	}
	return render(request,'dashboard/products.html',context)

@login_required
def product_delete(request,pk):
	item = Product.objects.get(id=pk)
	if request.method=="POST":
		item.delete()
		return redirect('dashboard-products')
	return render(request,'dashboard/product_delete.html')


@login_required
def product_update(request, pk):
	item = Product.objects.get(id=pk)
	if request.method=='POST':
		#instance is used to fetch data for particular id
		form = ProductForm(request.POST,instance=item)
		if form.is_valid():
			#to save form data to database
			form.save()
			return redirect('dashboard-products')
	else:
		form = ProductForm(instance=item)

	context={
		'form':form
	}
	return render(request,'dashboard/product_update.html', context)

@login_required
def category(request):
	category = Category.objects.all()
	if request.method=='POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('dashboard-category')	
	else:
		form = CategoryForm()
	context={
		'form':form,
		'category':category,
	}
	return render(request,'dashboard/category.html',context)


@login_required
def orders(request):
	order = Order.objects.all()
	staff = User.objects.all()

	if request.method=='POST':
		form =OrderForm(request.POST)
		if form.is_valid():
			#these three lines are used to send the data of staff member who orders the product
			instance = form.save(commit=False)
			instance.staff = request.user
			instance.save()
			order_id = instance.id
			order_qty = instance.order_quantity
			prodId=instance.product_id
			product_qty = list(Product.objects.filter(id=prodId).values())[0]['quantity']
			updated_qty = order_qty+product_qty
			Product.objects.filter(id=prodId).update(quantity=updated_qty)
			product_name = form.cleaned_data.get('product')
			orderQty = form.cleaned_data.get('order_quantity')
			messages.success(request,f'Order of {orderQty} { product_name} has been placed')
			return redirect('dashboard-orders')
	else:
		form = OrderForm()

	context={
		'order':order,
		'staff':staff,
		'form':form,
	}
	return render(request,'dashboard/orders.html',context)

def customer(request):
	customer = Customer.objects.all()
	# item = Product.objects.get(id=pk)

	if request.method=='POST':
		form =CustomerForm(request.POST)
		if form.is_valid():

			#these three lines are used to send the data of staff member who orders the product
			instance = form.save(commit=False)
			instance.save()
			customer_id = instance.id
			order_qty = instance.quantity
			prodId=instance.product_id
			product_qty = list(Product.objects.filter(id=prodId).values())[0]['quantity']
			updated_qty = product_qty-order_qty
			Product.objects.filter(id=prodId).update(quantity=updated_qty)
			return redirect('dashboard-customer')
	else:
		form = CustomerForm()

	context={
		'customer':customer,
		'form':form,
	}
	return render(request,'dashboard/customer.html',context)


# export product details excel file

@login_required
def export_product_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="product_details.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Product')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Category', 'Quantity','Amount_per_product','Description',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Product.objects.all().values_list('name','category__name', 'quantity', 'amount_per','description')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

# export staff details to excel file

@login_required
def export_staff_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="staff_details.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Profile')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Username', 'Address', 'Phone No', 'Email']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Profile.objects.all().values_list('staff__username', 'address', 'phone','staff__email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


# export order details to excel file

@login_required
def export_order_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="order_details.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Order')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Product Name', 'Ordered By', 'Quantity',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Order.objects.all().values_list('product__name', 'staff__username', 'order_quantity')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


