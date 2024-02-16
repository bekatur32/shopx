from rest_framework import serializers
from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
        extra_kwargs = {'sender': {'read_only': True, }, 'timestamp': {'read_only': True, },
                        'chat': {'read_only': True, }, }


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('participants', )
        extra_kwargs = {'participants': {'read_only': True, }, }
