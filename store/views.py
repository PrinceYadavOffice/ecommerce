from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail.message import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from .models import *
from .forms import LoginForm,RegistrationForm
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.template import Context
from django.template.loader import get_template, render_to_string


# Create your views here.

class FilterProducts(ListView):
    template_name = "store/index.html"
    model = Product
    context_object_name = "product"

    def get_queryset(self):      
        qs=self.kwargs['qs']  
        return self.model.objects.all().order_by(f"{qs}")

class IndexView(View):
    template_name = "store/index.html"
    model = Product

    def post(self, request):
        searchItem = request.POST["searchItem"]
        if searchItem != "":
            products = self.model.objects.filter(Q(type=searchItem) | Q(name__icontains=searchItem))
        else:
            products = self.model.objects.all()
        context = {
        'product' : products
        }
        return render(request, self.template_name, context)

    def get(self, request):
        products = self.model.objects.all()
        context = {
        'product' : products
        }
        return render(request, self.template_name, context)


class UserProfile(LoginRequiredMixin, View):
    template_name = "store/profile.html"
    login_url = "/login"    

    def get(self, request):
        items=[]
        customer = request.user.customer
        orders = Order.objects.all().filter(customer=customer, complete=True)     
        for order in orders:
            for item in order.cartitems_set.all():
                items.append(item)   
        context ={
            'items':items
        }
        return render(request, self.template_name,context)


class Checkout(LoginRequiredMixin,TemplateView):
    template_name = "store/checkout.html"
    login_url = "/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = Order.objects.get(customer=self.request.user.customer, complete=False) 
        context["items"] = context["order"].cartitems_set.all()
        return context


class PlaceOrder(LoginRequiredMixin, View):
    template_name = "store/place-order.html"
    login_url = "/login"

    def get(self, request, id):
        customer = request.user.customer
        order = Order.objects.get(customer=customer,id=id)
        order.complete = True          
        shipping = Shipping_Order.objects.create(order=order, shippingAddress = customer.get_complete_address)    
        shipping.save()
        order.save()
        items = order.cartitems_set.all()  
        subject = "Your Order is Placed | Online Shopping"
        toemail = customer.user.email        
        context = {'order': order, 'items': items}
        # html = get_template('store/orderemail.html')
        # html_content = html.render(context)    
        message = render_to_string('store/orderemail.html', context)        
        msg = EmailMessage(subject, message,settings.EMAIL_HOST_USER, to=[toemail,])
        # msg.attach_alternative(html_content, 'text/html')
        msg.content_subtype = 'html'
        msg.send()
        
        return render(request, self.template_name, {'id':id})


class CartView(LoginRequiredMixin, View):
    template_name = "store/cart.html"
    login_url = "/login"

    def get(self, request):
        customer = request.user.customer
        try:
            order = Order.objects.get(customer=customer, complete=False) 
            items = order.cartitems_set.all()  
        except:
            items =[]   

        context ={
            'items':items
        }
        return render(request, self.template_name,context)


class UserRegister(View):    
    template_name = "store/register.html"

    def get(self, request):
        form = RegistrationForm()
        return render(request,  self.template_name, {'form':form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        username = request.POST["username"]
        email = request.POST["email"]
        if form.is_valid():
            form.save()
            messages.info(request,"Registration Successful")
            subject = 'welcome to Online Shopping'
            message = f'Hi {username}, thank you for registering in online shopping.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )            
            return redirect('login')   


class UserLogin(View):
    def post(self, request):                
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=email)
        except:
            messages.info(request,"Invalid Credentials")
            return redirect('login')

        user = authenticate(request, username=user.username, password=password)
        if user != None:            
            login(request, user)
            return redirect("/")
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('login')

    def get(self, request):                    
        form = LoginForm()                    
        return render(request, "store/login.html", {"form": form}) 


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect("/")

class ProductDetail(View):
    def get(self,request,slug):       
        product = Product.objects.get(slug=slug)    
        status = "Available"
        if product.total_units < 1 :
            status = "Out Of Stock"

        context={
            'product':product,
            'status':status        
        }    
        return render(request,'store/product_details.html', context)    

@login_required(login_url='/login')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('ProductId: ',productId, 'action: ',action)

    customer = request.user.customer
    print("test 2 pass")
    product = Product.objects.get(id=productId)
    print("test 3 pass")
    try:
        order = Order.objects.get(customer=customer, complete=False)
    except:
        order = Order.objects.create(customer=customer)   
    
    print("test 4 pass order id: ",order)
    cartItem = CartItems.objects.get_or_create(order=order,product=product)
    print("test 5 pass cartitems: ", cartItem)
    
    if action == 'add' and  product.total_units != 0:
        cartItem[0].quantity += 1 
        product.total_units -= 1
       
    elif action == 'remove':
        cartItem[0].quantity -= 1 
        product.total_units += 1       

    cartItem[0].save()
    product.save() 

    if cartItem[0].quantity <=0:
        cartItem[0].delete()
        
    elif action == 'delete':
        quantity = cartItem[0].quantity
        cartItem[0].delete()
        product.total_units +=quantity

    product.save()          

    return JsonResponse('Item was added', safe=False)


    
def emailView(request):

    return render(request, 'store/orderemail.html')
