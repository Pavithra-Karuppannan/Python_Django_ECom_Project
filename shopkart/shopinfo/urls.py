from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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

    # API urls
    path('api/products/', views.product_list, name='api_products'),
    path('api/products/<int:pk>/', views.product_detail, name='api_product_detail'),
    path('api/cart/', views.cart_list, name='api_cart'),
    path('api/search/', views.search_api, name='api_search'),

     # JWT Auth urls
    path('api/login/', TokenObtainPairView.as_view(), name='api_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
]
