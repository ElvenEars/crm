from django.urls import path, re_path
from . import views

app_name='projects'
urlpatterns = [
    path('products/', views.products_list, name='products_list'),
    path('companies/', views.companies_list, name='companies_list'),
    path('', views.projects_list, name='projects_list'),
    path('filters/', views.projects_filters, name='products_filters'),
    path('create/', views.ProjectCreate.as_view(), name='project_create'),
    path('<slug:slug>/', views.project_detail, name='project_detail'),
    path('<slug:slug>/update/', views.ProjectUpdate.as_view(), name='project_update'),
    path('<slug:slug>/delete/', views.ProjectDelete.as_view(), name='project_delete'),

]