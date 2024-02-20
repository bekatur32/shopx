from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .usermanager import CustomUserManager
from .validators import validate_password_strength

class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = {
        'Мужчина':'Мужчина',
        'Женщина':'Женщина',
        'Другое':'Другое',
    }
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES.items())
    username = models.CharField(max_length= 30, verbose_name="Имя",null=True, blank=True)
    surname = models.CharField(max_length= 30, verbose_name="Фамилия",null=True, blank=True)
    password = models.CharField("password",validators=[validate_password_strength], max_length=128)
    email_or_phone = models.CharField(max_length= 30,unique = True,null= True, blank=True)
    code = models.CharField(max_length=6)
    created_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    number = models.CharField(max_length= 30,unique=True,null= True, blank=True)
    is_seller = models.BooleanField(default=False, verbose_name="продавец")

    objects = CustomUserManager()


    def __str__(self) -> str:
        return f"{self.username}"
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = verbose_name

    USERNAME_FIELD = 'email_or_phone'
    REQUIRED_FIELDS = ['username']



class SellerProfile(CustomUser):
    market_name = models.CharField(max_length = 50)
    image = models.ImageField(upload_to='media/profiles')
    category=models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    instagram_link = models.URLField()
    whatsapp_link = models.URLField()
    tiktok_link = models.URLField()
    facebook_link = models.URLField()

    def __str__(self) -> str:
        return f'Профиль продавца {self.username}'
    
    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = verbose_name

