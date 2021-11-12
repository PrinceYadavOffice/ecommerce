from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('checkout', views.checkout, name="checkout"),
    path('profile', views.profile, name="user-profile"),
    path('cart', views.cart, name="cart"),
    path('register', views.register, name="register"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout")
]
