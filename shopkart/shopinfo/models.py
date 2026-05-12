from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def getFilename(request,filename):
    current_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(current_time,filename)
    return os.path.join('uploads/',new_filename)

class Category(models.Model):
    category_name = models.CharField(max_length=150,null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text='0-show,1-hidden')
    category_image=models.ImageField(upload_to=getFilename,null=True,blank=True)
    created_dttm=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

class Products(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=150,null=False,blank=False)
    vendor_name = models.CharField(max_length=150,null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text='0-show,1-hidden')
    trending_product=models.BooleanField(default=False,help_text='0-default,1-trending')
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    product_image=models.ImageField(upload_to=getFilename,null=True,blank=True) 
    created_dttm=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  product=models.ForeignKey(Products,on_delete=models.CASCADE)
  product_qty=models.IntegerField(null=False,blank=False)
  created_at=models.DateTimeField(auto_now_add=True)

  @property
  def total_cost(self):
    return self.product_qty*self.product.selling_price
  
class Favourite(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Products,on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)