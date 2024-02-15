from rest_framework import serializers
from .models import *

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','surname','email','password']

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user
        
    
    
class SellerRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ['username','surname','email','password','market_name']

    def create(self, validated_data):
        user = Seller.objects.create_user(**validated_data)
        user.is_seller = True
        user.save()
        return user
    
    
# class WholeSellerRegisterSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = WholeSeller
#         fields = ['username','surname','email','password','question_for_wholeseller']

#     def create(self, validated_data):
#         user = WholeSeller.objects.create_user(**validated_data)
#         user.wholeseller = True
#         user.save()
#         return user




class VerifyCodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['code']


class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email','password']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)
    
    class Meta:
        fields = ['old_password','new_password','confirm_new_password',]

class SendCodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email']


class ForgetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=20,write_only=True)
    confirm_password = serializers.CharField(max_length=20,write_only=True)

    class Meta:
        fields = ['password','confirm_password']



class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['username',
                  'surname',
                  'email',
                  'number',
                  'gender',
                  'category',
                  'location',
                  'whatsapp_link',
                  'instagram_link',
                  'tiktok_link']
    