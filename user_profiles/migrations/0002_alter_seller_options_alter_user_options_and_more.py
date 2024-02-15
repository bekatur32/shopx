# Generated by Django 4.2.10 on 2024-02-15 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user_profiles", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="seller",
            options={"verbose_name": "Продавцы", "verbose_name_plural": "Продавцы"},
        ),
        migrations.AlterModelOptions(
            name="user",
            options={
                "verbose_name": "Пользователи",
                "verbose_name_plural": "Пользователи",
            },
        ),
        migrations.AlterModelOptions(
            name="userprofile",
            options={"verbose_name": "Профили", "verbose_name_plural": "Профили"},
        ),
        migrations.DeleteModel(
            name="WholeSeller",
        ),
    ]
