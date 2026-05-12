from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name','category_image','description')

admin.site.register(Category,CategoryAdmin)

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'vendor_name', 'category','product_image')
    
admin.site.register(Products, ProductsAdmin)


