from rest_framework import serializers
from .models import Product, Recall


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "podcategory",
            "name",
            "image",
            "description",
            "price",
        )
        read_only_fields = (
            "id",
            "slug",
            "user",
            "created",
            "updated",
        )  # Поля, которые можно только читать


class ProductSerializer(serializers.ModelSerializer):
    location = serializers.CharField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'category', 'podcategory', 'user', 'name', 'slug', 'image', 'description', 'price', 'location', 'rating',
            'available', 'created', 'updated'
        )
        read_only_fields = ('id', 'slug', 'user', 'created', 'updated')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        include_location_rating = self.context.get('include_location_rating', False)
        if not include_location_rating:
            representation.pop('location', None)
            representation.pop('rating', None)

        return representation


class RecallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recall
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True, }, 'created': {'read_only': True, },
                        'updated': {'read_only': True, },
                        }
