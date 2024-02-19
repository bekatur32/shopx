from rest_framework import serializers
from .models import Category, PodCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "img")
    #    read_only_fields = ("id", "slug")  # Поля, которые можно только читать


class PodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PodCategory
        fields = ("id", "name", "category")
    #    read_only_fields = ("id", "slug")