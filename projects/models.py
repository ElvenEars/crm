from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from unidecode import unidecode
from django.utils.text import slugify
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime, timedelta, date

class Category(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=300, db_index=True, unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', verbose_name="Категория",  on_delete=models.CASCADE,)
    code = models.CharField(max_length=15, db_index=True, verbose_name="код")
    name = models.CharField(max_length=300, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    available = models.BooleanField(default=True, verbose_name="Активность")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name="Цена", default=0)
    
    class Meta:
        verbose_name = 'Продукция'
        verbose_name_plural = 'Продукция'
    
    def __str__(self):
        return self.name + " " + self.description
    
    def toStringName (self): 
        return self.name
class Company(models.Model):
    full_name = models.CharField(max_length=300, db_index=True, verbose_name="Полное наименование")
    short_name = models.CharField(max_length=300, db_index=True, verbose_name="Краткое наименование")
    slug = models.SlugField(max_length=200,  blank=True)
    inn = models.DecimalField(blank=True, max_digits=13, decimal_places=0, verbose_name="ИНН", default=0)   
    license_adress = models.TextField(blank=True, verbose_name="Юридический адрес")    
    adress = models.TextField(verbose_name="Фактический дарес с индексом") 
    phone = models.CharField(max_length=100, verbose_name="Телефон") 
    email = models.CharField(max_length=100, db_index=True, verbose_name="Email")
    site = models.CharField(max_length=100, db_index=True, verbose_name="Сайт")
    license_date = models.DateField( verbose_name="Срок действия лицензионного сертификта")
    license_upload = models.FileField(upload_to='upload/', verbose_name='Лицензия')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компания'

    def check_license(self):
        return self.license_date > date.today() 
    def sum_software(self):
        projects = Project.objects.filter(user__company = self.pk)
        sum = 0
        for project in projects:
            sum = sum + project.get_full_price()
        return sum
    def sum_full_companies(self):
        sum =0 
        for project in Project.objects.all():
            sum = sum + project.get_full_price()
        return sum
    def __str__(self):
        return self.short_name

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True ,)
    phone = models.CharField(max_length=30, blank=True)
   
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профиль пользователя'
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    

class Project(models.Model):
    MANAGER_STATUS = (
        (0, 'проект'),
        (1, 'в работе'),
        (2, 'окончен'),
        (3, 'отменен'),
    )
    NEOCOM_STATUS = (
        (0,'на расмотрении'),
        (1,'одобрен'),
        (2,'не одобрен'),
    )
    id=models.AutoField(primary_key=True)
    manager_status = models.IntegerField(choices = MANAGER_STATUS, default = MANAGER_STATUS[0][0], verbose_name="Статус проекта")
    neocom_status = models.IntegerField(choices = NEOCOM_STATUS, default = NEOCOM_STATUS[0][0], verbose_name="Статус Neocom")
    project_name = models.CharField(max_length=300, db_index=True, verbose_name="Название проекта")
    slug = models.SlugField(max_length=200,  blank=True)
    inn = models.DecimalField(max_digits=13, decimal_places=0, verbose_name="ИНН")
    end_customer = models.CharField(max_length=300, default="", verbose_name="Конечный заказчик")
    probability = models.DecimalField(max_digits=3, decimal_places=0, verbose_name="Вероятность реализации")
    contacts = models.TextField(blank=True, verbose_name="контактные данные")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True)
    end_date = models.DateField(blank=True, verbose_name="Дата окончания проекта")
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True ,)
    
    class Meta:
        verbose_name = 'Проекты'
        verbose_name_plural = 'Проекты'

    def user_profile(self):
        return self.user.profile

    def __str__(self):
        return self.project_name

    def get_neocom_status(self):
        return self.NEOCOM_STATUS[self.neocom_status][1]
    
    def get_manager_status(self):
        return self.MANAGER_STATUS[self.manager_status][1]
    
    def _get_unique_slug(self):
        slug = slugify(unidecode(self.project_name), allow_unicode=True)
        unique_slug = slug
        num = 1
        while Project.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def get_absolute_url(self):
        return reverse('projects:project_detail',
                        args=[self.slug])
    
    def __unicode__(self):
        return self.project_name

    def get_full_price(self):
        orders = OrderItem.objects.filter(project=self.pk)
        full_price = 0
        for o in orders: 
            full_price = full_price + o.get_order_price()
        return round(float(full_price),3)

    def get_full_internal_price(self):
        orders = OrderItem.objects.filter(project=self.pk)
        full_price = 0
        for o in orders: 
            full_price = full_price + (o.get_product_buying_price()*o.quantity)
        return round(float(full_price),3)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        #send_mail('Тема', 'Тело письма', settings.EMAIL_HOST_USER, ['i.tarasov@neocomspb.ru'])
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    project= models.ForeignKey(Project, related_name='orderitems', on_delete=models.CASCADE, default="")
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE, verbose_name="Продукт")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def add_in_view(self, project, product, price, quantity):
        self.project = project
        self.product = product
        self.quantity = quantity
        self.price = price
    
    def get_product_buying_price(self):
        if (self.product.category.slug == "dispetcherskoe-programmnoe-obespechenie-trbonet-enterprise"):
            return round(float(self.product.price)*0.35,2)
        else:
            return round(float(self.product.price)*0.6,2)
    def get_product_price(self):
        return round(float(self.product.price),2)

    def get_order_price(self):
        return round(float(self.product.price*self.quantity)*0.7,2)

    def save (self, *args, **kwargs):   
        orders = OrderItem.objects.filter(project = self.project)
        for order in orders:
            if order.product == self.product and order.pk != self.pk:
                order.quantity = order.quantity + self.quantity
                order.save()
                return
        super(OrderItem, self).save(*args,**kwargs)

    class Meta: 
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиция'
    def __str__(self):
        return self.product.name


    
# Create your models here.
