from django.urls import path
from . import views

urlpatterns = [
    path('detail/<str:pid>', views.detail, name='detail'),
    path('shop', views.shop, name='shop'),
    path('profile', views.profile, name='profile'),
    path('productdetail', views.productJsonDetail, name='productdetail'),
    path('shop/products', views.shoppagedata, name='shoppagedata'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('', views.homepage, name='homepage')
]