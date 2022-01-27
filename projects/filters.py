import django_filters
from django import forms
from .models import Project, Product 
from crispy_forms.helper import FormHelper

class ProjectFilter(django_filters.FilterSet):
	neocom_status = django_filters.ChoiceFilter(choices=Project.NEOCOM_STATUS, widget=forms.Select(attrs={'class': 'form-control-small'}))
	manager_status = django_filters.ChoiceFilter(choices = Project.MANAGER_STATUS, widget=forms.Select(attrs={'class': 'form-control-small'}))
	#manager_status = django_filters.ModelChoiceFilter(queryset= Project.user.ob, widget=forms.Select(attrs={'class': 'form-controlsmall'}))
	class Meta:
		model = Project
		fields = {'manager_status','neocom_status', 'user__company', 'user'}

class ProjectAdminFilter(django_filters.FilterSet):
	project_name = django_filters.CharFilter(field_name='project_name',lookup_expr='icontains',  widget=forms.TextInput(attrs={'class': 'form-control'}))
	products = django_filters.ModelMultipleChoiceFilter(field_name='orderitems__product',  queryset = Product.objects.all())
	manager_status = django_filters.ChoiceFilter(choices = Project.MANAGER_STATUS, widget=forms.Select(attrs={'class': 'select form-control'}))
	inn = django_filters.CharFilter(field_name='inn',lookup_expr='exact', widget=forms.TextInput(attrs={'class': 'form-control'}))
	neocom_status = django_filters.ChoiceFilter(choices=Project.NEOCOM_STATUS, widget=forms.Select(attrs={'class': 'select form-control'}))
	
	class Meta:
		model = Project
		fields = {'manager_status','neocom_status','inn','products'}
	
