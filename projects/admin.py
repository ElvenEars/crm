from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Category, Product, Project, OrderItem, Profile, Company
from django.forms import TextInput, Textarea
from django.db import models
from admin_auto_filters.filters import AutocompleteFilter
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['short_name','inn','license_date']
    prepopulated_fields = {'slug': ('full_name',)} 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code','name','description','price','available', 'created']
    list_filter = ['category__name','available']
    list_editable = ['available']
    search_fields = ('code','name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    
   
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 1

'''@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product','price','quantity']
    search_fields = ['product']'''

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['user','end_customer','inn','project_name','manager_status','probability','created','end_date']
    list_filter = [
        ('project_name'),
        ('manager_status'),
        ('neocom_status'),
        ('inn'),
        ('end_date'),
    ]
    '''fieldsets = [
        ('Название',{'fields':['project_name']}),
        
    ]'''
    radio_fields = {"manager_status": admin.VERTICAL}
    inlines = [OrderItemInline]
    list_per_page = 20



class UserInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Доп. информация'
    
class UserProfileAdmin(UserAdmin):
    inlines = (UserInline, )

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)

# Register your models here.
