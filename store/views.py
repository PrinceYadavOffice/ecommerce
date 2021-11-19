from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import *
from .forms import LoginForm,RegistrationForm,SetquantityForm
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Q

# Create your views here.



def index(request):
    products = Product.objects.all()
    if request.method == "POST":
        searchItem = request.POST["searchItem"]
        if searchItem != "":
            products = Product.objects.filter(Q(type=searchItem) | Q(name__icontains=searchItem))
        
        context = {
        'product' : products
        }
        return render(request, 'store/index.html', context)    
    context = {
        'product' : products
    }
    return render(request, 'store/index.html', context)    

@login_required(login_url='/login')
def profile(request):
    items=[]
    customer = request.user.customer
    orders = Order.objects.all().filter(customer=customer)     
    for order in orders:
        for item in order.cartitems_set.all():
            items.append(item)   
    context ={
        'items':items
    }
    return render(request, 'store/profile.html',context)

@login_required(login_url='/login')
def checkout(request):
    customer = request.user.customer
    order = Order.objects.get(customer=customer)    
    items = order.cartitems_set.all()
    context={
        'items':items,
        'order':order
    }
    return render(request, 'store/checkout.html', context)

@login_required(login_url='/login')
def cart(request):
    customer = request.user.customer
    order = Order.objects.get(customer=customer)
    items = order.cartitems_set.all()
    #items=[]
    context ={
        'items':items
    }

    return render(request, 'store/cart.html',context)            

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,"Registration Successful")            
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'store/register.html', {'form': form})    
   

def user_login(request):        
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user != None:            
            login(request, user)
            return redirect("/")
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('login')    
    form = LoginForm()                    
    return render(request, "store/login.html", {"form": form})    
    
	

def user_logout(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")


def product_detail(request, slug):
    form = SetquantityForm()    
    product = Product.objects.get(slug=slug)    
    status = "Available"
    if product.total_units < 1 :
        status = "Out Of Stock"

    context={
        'product':product,
        'status':status        
    }    
    return render(request,'store/product_details.html', context)    


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('ProductId: ',productId, 'action: ',action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer)
    cartItem, created = CartItems.objects.get_or_create(order=order,product=product)

    if action == 'add' and cartItem.quantity < product.total_units:
        cartItem.quantity = (cartItem.quantity + 1)
    elif action == 'remove':
        cartItem.quantity = (cartItem.quantity -1)       

    cartItem.save() 

    if cartItem.quantity <=0:
        cartItem.delete()  
    elif action == 'delete':
        cartItem.delete()      

    return JsonResponse('Item was added', safe=False)