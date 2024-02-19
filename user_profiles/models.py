from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from product.models import Product
from .usermanager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length= 30, verbose_name="Имя",null=True, blank=True)
    surname = models.CharField(max_length= 30, verbose_name="Фамилия",null=True, blank=True)
    email_or_phone = models.CharField(max_length= 30,unique = True,null= True, blank=True)
    code = models.CharField(max_length=6)
    created_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    number = models.CharField(max_length= 30,unique=True,null= True, blank=True)
    is_seller = models.BooleanField(default=False, verbose_name="продавец")

    objects = CustomUserManager()


    def __str__(self) -> str:
        return f"{self.username}"

    USERNAME_FIELD = 'email_or_phone'
    REQUIRED_FIELDS = ['username']



class UserProfile(CustomUser):
    GENDER_CHOICES = {
        'Мужчина':'Мужчина',
        'Женщина':'Женщина',
        'Другое':'Другое',
    }
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES.items())
    image = models.ImageField(upload_to='media/profiles')
    category=models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    instagram_link = models.URLField()
    whatsapp_link = models.URLField()
    tiktok_link = models.URLField()
    facebook_link = models.URLField()

    def __str__(self) -> str:
        return f'Профиль пользователя '
    
    class Meta:
        verbose_name = 'Профили '
        verbose_name_plural = verbose_name


class User(UserProfile):

    def __str__(self) -> str:
        return f'{self.username} Покупатель'
    
    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = verbose_name
63


class Seller(UserProfile):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    market_name = models.CharField(max_length=30) 
    
    def __str__(self) -> str:
        return f'{self.username} Продавец'
    
    class Meta:
        verbose_name = 'Продавцы'
        verbose_name_plural = verbose_name



# class WholeSeller(UserProfile):
#     question_for_wholeseller = models.CharField(max_length = 30, verbose_name = "вопрос для оптовика")
    

#     def __str__(self) -> str:
#         return f'{self.username} Оптовик'