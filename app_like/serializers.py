from rest_framework import serializers
from app_like.models import Like

class LikeSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)

class LikeModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'