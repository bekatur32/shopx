from rest_framework import serializers
from .models import *

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email_or_phone','password']


    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user
        
    
    
class SellerRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ['email_or_phone','password','market_name','location']

    def create(self, validated_data):
        user = Seller.objects.create_user(**validated_data)
        user.is_seller = True
        user.save()
        return user
    


class VerifyCodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['code']


class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email_or_phone','password']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)
    
    class Meta:
        fields = ['old_password',
                  'new_password',
                  'confirm_new_password',]

class SendCodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email_or_phone']


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
                  'email_or_phone',
                  'number',
                  'gender',
                  ]
        
class SellerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ['number',
                  'market_name',
                  'location',
                  'email_or_phone',
                  'category',
                  'instagram_link',
                  'whatsapp_link',
                  'tiktok_link',
                  'facebook_link',
                  ]
        
