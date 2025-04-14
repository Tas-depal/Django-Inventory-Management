from django.urls import path

#manually added
from . import views


#manually added
urlpatterns = [
    path('dashboard/', views.index, name='dashboard-index'),
    path('staff/',views.staff, name='dashboard-staff'),
    path('staff_detail/<int:pk>/',views.staff_detail, name='dashboard-staff-detail'),
    path('products/',views.products,name='dashboard-products'),
    path('category/',views.category,name='dashboard-category'),
    path('product_update/<int:pk>/',views.product_update,name='dashboard-product-update'),
    path('product_delete/<int:pk>/',views.product_delete,name='dashboard-product-delete'),
    path('orders/',views.orders,name='dashboard-orders'),
    path('dashboard-customer/',views.customer,name='dashboard-customer'),
    path(r'^export/xls1/$', views.export_product_xls, name='export_product_xls'),
    path(r'^export/xls2/$', views.export_order_xls, name='export_order_xls'),
    path(r'^export/xls3/$', views.export_staff_xls, name='export_staff_xls'),
]
