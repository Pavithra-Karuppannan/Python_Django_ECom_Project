from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
     path('search', views.search_view,name='search'),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('products',views.products,name="products"),
    path('cart',views.cart_page,name="cart"),
    path('addtocart',views.add_to_cart,name="addtocart"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('fav',views.fav_page,name="fav"),
    path('favviewpage',views.favviewpage,name="favviewpage"),
    path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav"),
    path('products/<str:category>',views.productsview,name="products"),
    path('products/<str:cname>/<str:pname>',views.productDetails,name="productDetails"),
]
