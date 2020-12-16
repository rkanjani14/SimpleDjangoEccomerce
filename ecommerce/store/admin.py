from django.contrib import admin

# Register your models here.
from .models import *
# Old method 
# admin.site.register(customer)
# admin.site.register(product)
# admin.site.register(order)
# admin.site.register(order_item)
# admin.site.register(shipping_address)

# New Method
@admin.register(product)
class productAdmin(admin.ModelAdmin):
    list_display = ['id','name','price','digital','image']

@admin.register(order)
class orderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','date_ordered','complete','transcation_id']

@admin.register(order_item)
class order_itemAdmin(admin.ModelAdmin):
    list_display = ['id','product','order','quantity','date_added']

@admin.register(shipping_address)
class shipping_address(admin.ModelAdmin):
    list_display = ['id','customer','order','address','city','state','zipcode','date_added']

@admin.register(customer)
class customerAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','email']
