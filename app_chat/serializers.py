from rest_framework import serializers
from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
        extra_kwargs = {'sender': {'read_only': True, }, 'timestamp': {'read_only': True, },
                        'chat': {'read_only': True, }, }


class ChatSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        exclude = ('participants', )

    def get_user(self, obj):
        user = obj.participants.exclude(pk=obj.user).first()
        return user.pk
