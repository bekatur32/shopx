from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated


class ChatViewSet(GenericViewSet):
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        queryset = Chat.objects.filter(participants__in=[self.request.user])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat = Chat.objects.create()
        chat.participants.add(self.request.user, serializer.validated_data['participants'])
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer.delete()
        return Response('Chat is deleted')


class MessageListApiView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.filter(chat=self.kwargs['pk'])
        return queryset


class MessageViewSet(GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat, created = Chat.objects.get_or_create(
            participants__in=[self.request.user, serializer.validated_data['participants']])
        serializer.save(sender=request.user, chat=chat)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        if instance.sender == self.request.user or instance.recipient == self.request.user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response('No access')

    def update(self, request, pk=None):
        instance = self.get_object()
        if instance.sender == self.request.user:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk=None)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        if instance.sender == self.request.user:
            instance.delete()
            return Response('Message is deleted')
