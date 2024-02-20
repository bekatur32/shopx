from rest_framework import serializers
from .models import Product, Recall, Discount


class ProductSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    category_name = serializers.SerializerMethodField()
    podcategory_name = serializers.SerializerMethodField()

    def get_category_name(self, obj):
        return obj.category.name if obj.category.name else None

    def get_podcategory_name(self, obj):
        return obj.podcategory.name if obj.podcategory.name else None

    class Meta:
        model = Product
        fields = (
            "id",
            'category_name',
            'podcategory_name',
            "category",
            "podcategory",
            "user",
            "title",
            "description",
            "price",
            "location",
            "image1",
            "image2",
            "image3",
            "image4"

        )
=======
    location = serializers.CharField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    likes = serializers.IntegerField(read_only=True)
>>>>>>> b7f160af6a5136430ea0163f929c712351a5f3d3

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
<<<<<<< HEAD
        fields = [
            'title',
            'price',
            'description',
            'location',
            "image1",
            "image2",
            "image3",
            "image4"
]
=======
        fields = (
            'id', 'category', 'podcategory', 'user', 'name', 'slug', 'image', 'description', 'price', 'location', 'rating',
            'available', 'created', 'updated', 'likes'
        )
        read_only_fields = ('id', 'slug', 'user', 'created', 'updated')

>>>>>>> b7f160af6a5136430ea0163f929c712351a5f3d3

class RecallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recall
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True, }, 'created': {'read_only': True, },
                        'updated': {'read_only': True, },
                        }

class DiscountSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = ['id', 'product', 'price', 'discount_rate', 'discounted_price']

    def get_discounted_price(self, obj):
        return obj.discounted_price()