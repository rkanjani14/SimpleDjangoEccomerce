from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *

# Create your views here.

def store(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order1,created = order.objects.get_or_create(customer=customer, complete=False) 
          items = order1.order_item_set.all()
          cartItems = order1.get_cart_items
     else:
          items = []
          order1 = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
          cartItems = order1['get_cart_items']

     products = product.objects.all()
     context = {'products':products,'cartItems':cartItems}
     return render(request, 'store/store.html', context)

def cart(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order1,created = order.objects.get_or_create(customer=customer, complete=False) 
          items = order1.order_item_set.all()
          cartItems = order1.get_cart_items
     else:
          try:
               cart = json.loads(request.COOKIES['cart'])
          except:
               cart = {}
          print('CART' ,cart)

          items = []
          order1 = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
          cartItems = order1['get_cart_items']
          for i in cart:
               cartItems += cart[i]['quantity']

     context = {'items':items,'order':order1,'cartItems':cartItems}
     return render(request, 'store/cart.html', context)

def checkout(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order1,created = order.objects.get_or_create(customer=customer, complete=False) 
          items = order1.order_item_set.all()
          cartItems = order1.get_cart_items
     else:

          items = []
          order1 = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
          cartItems = order1['get_cart_items']

     context = {'items':items,'order':order1,'cartItems':cartItems }
     return render(request, 'store/checkout.html', context)

def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']

     print('Action : ',action)
     print('productId : ',productId)

     customer = request.user.customer
     Product = product.objects.get(id=productId)
     Order,created= order.objects.get_or_create(customer=customer,complete=False)

     orderItem,created = order_item.objects.get_or_create(order=Order ,product=Product)

     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)
     
     orderItem.save()

     if orderItem.quantity <=0:
          orderItem.delete()

     return JsonResponse('item as added',safe=False)

def processOrder(request):
     transaction_id = int(datetime.datetime.now().timestamp())
     data = json.loads(request.body)
     print('transaction _id ',transaction_id)
     
     if request.user.is_authenticated:
          customer = request.user.customer
          Order,created = order.objects.get_or_create(customer=customer,complete=False)
          total = float(data['user_data']['total'])
          Order.transaction_id = str(transaction_id)

          if total == float(Order.get_cart_total):
               Order.complete=True
          Order.save()

          if Order.shipping == True:
               shipping_address.objects.create(
                    customer = customer,
                    order = Order,
                    address= data['shipping_info']['address'],
                    city = data['shipping_info']['city'],
                    state = data['shipping_info']['state'],
                    zipcode = data['shipping_info']['zipcode'],
               )

     else:
          print('User is not logged in ...')
     return JsonResponse('Payment completed',safe=False)




