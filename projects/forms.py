from django import forms
from .models import Project, OrderItem, Profile, Product
from django.forms.widgets import SelectDateWidget
from django.forms import CheckboxSelectMultiple
from django.forms.formsets import BaseFormSet
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {'user': forms.Select(attrs={'class': "select form-control"}),
                   'slug': forms.HiddenInput(),
                   'neocom_status': forms.HiddenInput(),
                   'manager_status' : forms.Select(attrs={'class': "select form-control"}),
                   'end_date' : forms.DateInput(attrs={'class': "mask-date form-control"}),
                   'project_name' : forms.DateInput(attrs={'class': "form-control"}),
                   'end_customer' : forms.DateInput(attrs={'class': "form-control"}),
                   'probability' : forms.DateInput(attrs={'class': "form-control"}),
                   'contacts' : forms.Textarea(attrs={'class': "form-control"}),
                   'inn' : forms.DateInput(attrs={'class': "inn-date form-control"})
                   }

    def __init__(self, *args, **kwargs):
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
    
class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {'user': forms.HiddenInput(),
                   'slug': forms.HiddenInput(),
                   'neocom_status': forms.HiddenInput(),
                   'manager_status' : forms.Select(attrs={'class': "select form-control"}),
                   'end_date' : forms.DateInput(attrs={'class': "mask-date form-control"}),
                   'project_name' : forms.DateInput(attrs={'class': "form-control"}),
                   'end_customer' : forms.DateInput(attrs={'class': "form-control"}),
                   'probability' : forms.DateInput(attrs={'class': "form-control"}),
                   'contacts' : forms.Textarea(attrs={'class': "form-control"}),
                   'inn' : forms.DateInput(attrs={'class': "inn-date form-control"})
                   }

    def __init__(self, *args, **kwargs):
        super(ProjectUpdateForm, self).__init__(*args, **kwargs)

class OrderForm (forms.ModelForm):
    class Meta: 
        model = OrderItem
        fields = ['product','quantity']
        widgets = {
                   'product': forms.Select(attrs={'class': "form-control"}), 
                   'quantity': forms.TextInput(attrs={'class':'form-control'}), 
                  }

OrderItemFormSet = inlineformset_factory(Project, OrderItem, form = OrderForm, )

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ()
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone',)