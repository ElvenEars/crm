from django.shortcuts import render, get_object_or_404
from .models import Product, Project, OrderItem, Company
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.utils.decorators import method_decorator 
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView
from .forms import ProjectCreateForm, ProjectUpdateForm, OrderItemFormSet
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import ProjectFilter, ProjectAdminFilter
from django.db import transaction
from django.shortcuts import redirect
from django.core.mail import send_mail

@login_required
def products_list(request):
    products = Product.objects.order_by('category')
    
    return render (request, 'projects/products_list.html', {'products':products})

@permission_required('projects.view_company')
def companies_list(request):
    companies = Company.objects.order_by('-created')
    paginator = Paginator( companies, 10)
    companies_list = paginator.page(request.GET.get('page',1))
    return render (request, 'projects/company_list.html', {'companies':companies_list})


@login_required
def projects_list(request):
    if request.user.is_superuser == False:
        #return redirect('/admin/')
        user = request.user.profile
        projects_list = Project.objects.filter(user=user.id).order_by('-created')
    else: 
        projects_list = Project.objects.order_by('-created')
    filter = ProjectFilter(request.GET, queryset = projects_list)
    paginator = Paginator(filter.qs, 10)
    projects = paginator.page(request.GET.get('page',1))
    return render (request, 'projects/projects_list.html', {'projects':projects,'filter':filter})

@user_passes_test(lambda u: u.is_superuser)
def projects_filters(request):
    projects_list = Project.objects.order_by('-created')
    products = Product.objects.order_by('category')
    for i in range(2,200):
        if request.GET.get('c-'+str(i)):
            projects_list = projects_list.filter(orderitems__product__pk = i, orderitems__quantity = request.GET['c-'+str(i)])
    filter = ProjectAdminFilter(request.GET, queryset = projects_list)
    paginator = Paginator(filter.qs, 10)
    projects = paginator.page(request.GET.get('page',1))
    
    return render (request, 'projects/projects_filter.html', {'projects':projects,'filter':filter,'products':products})


@login_required
def project_detail(request, slug):
    if request.user.is_superuser == False:
        user = request.user.profile
        project = get_object_or_404(Project, slug = slug, user = user.id)
    else: 
        project = get_object_or_404(Project, slug = slug)
    return render(request,
                  'projects/project_detail.html',
                  {'project': project})

class ProjectUpdate(UpdateView):
    model = Project
    template_name = 'projects/project_form.html'
    form_class = ProjectUpdateForm

    def get_context_data(self, **kwargs):
        data = super(ProjectUpdate, self).get_context_data(**kwargs)
        quantity = {}
        for order in OrderItem.objects.filter(project = self.get_object()):
            quantity[order.product.pk] = order.quantity
        data['quantity'] = quantity
        data['products'] = Product.objects.order_by('category')
        return data 
        
    @method_decorator(permission_required('projects.change_project'))
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectUpdate, self).dispatch(request)

    def form_valid(self, form):
        context = self.get_context_data()
        products = context['products']
        for product in products:
            try: 
                quantity = int(self.request.POST.get(str(product.pk) + '-quantity'))
            except:
                quantity = 0
            orders = OrderItem.objects.filter(project=self.get_object(),product=product)
            if len(orders)>0:
                if quantity > 0 and orders[0].quantity != quantity:
                    orders[0].quantity = quantity
                    orders[0].save()
                if quantity == 0:
                    orders[0].delete()
            elif quantity > 0:
                order = OrderItem(project=self.get_object(), product=product, price=0 , quantity = quantity )
                order.save()
        return super(ProjectUpdate, self).form_valid(form)

class ProjectCreate(CreateView):
    model = Project
    template_name = 'projects/project_form.html'
    form_class = ProjectCreateForm

    @method_decorator(permission_required('projects.add_project'))
    def dispatch(self, request):
        return super(ProjectCreate, self).dispatch(request)

    def get_initial(self):
        if self.request.user.is_superuser == False:
            self.initial.update({'user': self.request.user.profile})
        return super(ProjectCreate, self).get_initial()

   
class ProjectDelete(DeleteView):
    model = Project
    success_url = '/projects/' 
    @method_decorator(permission_required('projects.delete_project'))
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectDelete, self).dispatch(request)


# Create your views here.
