from django.http import  JsonResponse
from django.shortcuts import redirect,render
from shopinfo.forms import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json


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
