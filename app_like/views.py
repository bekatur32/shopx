from datetime import datetime

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import Http404
from app_like.models import Like
from app_like.serializers import LikeSerializer, LikeModelSerializers
from product.models import Product
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from app_like.permissions import IsAuthor


class LikeView(GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid(raise_exception=True):
            product_id = srz_data.validated_data['product_id']
            try:
                Like.objects.get(product__id=product_id, user=request.user)
                return Response({'message': 'this product already liked by you'}, status=status.HTTP_400_BAD_REQUEST)
            except Like.DoesNotExist:
                product = get_object_or_404(Product, pk=product_id, available=True)
                Like.objects.create(user=request.user, product=product, register_date=datetime.now())
                return Response({'message': 'liked success'}, status=status.HTTP_200_OK)


class LikeListApiView(ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeModelSerializers
    permission_classes = [permissions.IsAuthenticated]


class LikeDeleteApiView(APIView):
    permission_classes = [IsAuthor, permissions.IsAdminUser]
    serializer_class = LikeModelSerializers

    def get_object(self, pk):
        try:
            return Like.objects.get(pk=pk)
        except Like.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        message = "успешно удалено"
        return Response(str(message), status=status.HTTP_204_NO_CONTENT)
