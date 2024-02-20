# Generated by Django 4.2 on 2024-02-20 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user_profiles.usermanager
import user_profiles.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('gender', models.CharField(choices=[('Мужчина', 'Мужчина'), ('Женщина', 'Женщина'), ('Другое', 'Другое')], max_length=20)),
                ('username', models.CharField(blank=True, max_length=30, null=True, verbose_name='Имя')),
                ('surname', models.CharField(blank=True, max_length=30, null=True, verbose_name='Фамилия')),
                ('password', models.CharField(max_length=128, validators=[user_profiles.validators.validate_password_strength], verbose_name='password')),
                ('email_or_phone', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('code', models.CharField(max_length=6)),
                ('created_at', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('number', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('is_seller', models.BooleanField(default=False, verbose_name='продавец')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', user_profiles.usermanager.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SellerProfile',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('market_name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='media/profiles')),
                ('category', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=20)),
                ('instagram_link', models.URLField()),
                ('whatsapp_link', models.URLField()),
                ('tiktok_link', models.URLField()),
                ('facebook_link', models.URLField()),
            ],
            options={
                'verbose_name': 'Профили ',
                'verbose_name_plural': 'Профили ',
            },
            bases=('user_profiles.customuser',),
            managers=[
                ('objects', user_profiles.usermanager.CustomUserManager()),
            ],
        ),
    ]
