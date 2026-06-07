from django.http import  JsonResponse
from django.shortcuts import redirect,render
from shopinfo.forms import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Products, Cart, Favourite
from .serializers import ProductSerializer, CartSerializer, FavouriteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

def home(request):
    products=Products.objects.filter(trending_product=1)
    return render(request,"shop/index.html",{"products":products})

def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/favourite.html",{"fav":fav})
  else:
    return redirect("/")
 
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
 
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"shop/cart.html",{"cart":cart})
  else:
    return redirect("/")

def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Products.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)

def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            product_status=Products.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)

def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")

def logout_page(request):
   if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
   return redirect("/")

def login_page(request):
    if request.user.is_authenticated:
       return redirect("/")
    else:
        if request.method == "POST":
            name = request.POST.get("username")
            pwd = request.POST.get("password")
            user = authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in successfully")
                return redirect("/")
            else:
                messages.error(request,"User name or password is incorrect")
                return redirect("/login")
        return render(request,"shop/login.html")

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You can Login Now..!")
            return redirect('/login')
        else:
           messages.error(request,"Please correct the information")
    else:
        form = CustomUserForm()
    return render(request,"shop/register.html",{"form":form})

def products(request):
    category = Category.objects.filter(status=0)
    return render(request,"shop/products.html",{"category":category})

def productsview(request,category):
    if(Category.objects.filter(category_name=category,status=0)):
        products=Products.objects.filter(category__category_name=category)
        return render(request,"shop/products/index.html",{"products":products,"category_name":category})
    else:
        messages.warning(request,'No records found')
        return redirect('products')

def productDetails(request,cname,pname):
    if(Category.objects.filter(category_name=cname,status=0)):
      if(Products.objects.filter(product_name=pname,status=0)):
        products=Products.objects.filter(product_name=pname,status=0).first()
        return render(request,"shop/products/productDetails.html",{"products":products})
      else:
        messages.error(request,"No Such Produtct Found")
        return redirect('products')
    else:
      messages.error(request,"No Such Catagory Found")
      return redirect('products')

def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=Products.objects.all().filter(product_name__icontains=query).select_related('category')
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'shop/searchResult.html',{'products':products,'query':query,'word':word,})
    else:
       return redirect('/login') 
    # ───── PRODUCTS ─────

# GET all products / POST new product
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET / PUT / DELETE single product
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Products.objects.get(pk=pk)
    except Products.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)


# ───── CART ─────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def cart_list(request):
    if request.method == 'GET':
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ───── SEARCH ─────

@api_view(['GET'])
def search_api(request):
    query = request.GET.get('query', '')
    products = Products.objects.filter(product_name__icontains=query)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

