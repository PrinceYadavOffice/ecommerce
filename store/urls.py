from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="home"),
    path('checkout', views.Checkout.as_view(), name="checkout"),
    path('profile', views.UserProfile.as_view(), name="user-profile"),
    path('cart', views.CartView.as_view(), name="cart"),
    path('register', views.UserRegister.as_view(), name="register"),
    path('login', views.UserLogin.as_view(), name="login"),
    path('logout', views.UserLogout.as_view(), name="logout"),
    path('product/<slug:slug>', views.ProductDetail.as_view(), name="product_detail"),
    path('update_item', views.updateItem, name="update_item"),
    path('place-order/<int:id>', views.PlaceOrder.as_view(), name="placeorder"),
    path('filter/<str:qs>', views.FilterProducts.as_view(), name="filter"),
    path('emailtemplate', views.emailView, name="email")
]
