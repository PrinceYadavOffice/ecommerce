from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from .forms import CustomUserCreationForm

# Create your views here.

def index(request):
    products = Product.objects.all()
    context = {
        'product' : products
    }
    return render(request, 'store/index.html', context)

def profile(request):
    return render(request, 'store/profile.html')

def checkout(request):
    return render(request, 'store/checkout.html')

def cart(request):
    return render(request, 'store/cart.html')            

def register(request):
    print(request.method)
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
	    form = AuthenticationForm(request, data=request.POST)
	    if form.is_valid():
		    username = form.cleaned_data.get('username')
		    password = form.cleaned_data.get('password')
		    user = authenticate(username=username, password=password)
		    if user is not None:
			    login(request, user)
			    messages.info(request, f"You are now logged in as {username}.")
			    return redirect("/")
		    else:
			    messages.info(request,"Invalid username or password.")
    form = AuthenticationForm()            
    context={
        'form':form
    }
    return render(request, 'store/login.html',context)	
	

def user_logout(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")

