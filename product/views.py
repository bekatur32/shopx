from rest_framework.response import Response
from .serializers import ProductSerializer, RecallSerializer
from .models import Product, Recall
from rest_framework.viewsets import GenericViewSet


from .serializers import ProductSerializer, ProductDetailSerializer
from .permissions import IsSellerOfProduct, IsAdminOrOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Product, Recall, Like
from user_profiles.permissions import IsSeller, IsBuyer
from .filters import CustomFilter
from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ProductsByPodCategoryApiView(APIView):
    def get(self, request, podcategory_id):
        products = Product.objects.filter(podcategory_id=podcategory_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductsByCategoryApiView(APIView):
    def get(self, request, category_id):
        products = Product.objects.filter(category_id=category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductCreateApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    permission_classes = [IsSeller, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all().annotate(rating=Avg("recall__rating"), likes=Count('like'))
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "podcategory", "user", "price", "available"]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "price"]
    permission_classes = [AllowAny, ]



class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly, ]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CustomFilter
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price"]


# Представление для получения деталей, обновления и удаления продукта
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().annotate(rating=Avg("recall__rating"), likes=Count('like'))
    serializer_class = ProductSerializer
    permission_classes = [IsSeller, ]


class RecallListApiView(ListAPIView):
    serializer_class = RecallSerializer

    def get_queryset(self):
        queryset = Recall.objects.filter(product=self.kwargs['pk'])
        return queryset


class RecallViewSet(GenericViewSet):
    queryset = Recall.objects.all()
    serializer_class = RecallSerializer
    permission_classes = [IsBuyer, ]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        if instance.user == self.request.user:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk=None)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        if instance.user == self.request.user:
            instance.delete()
            return Response('Recall is deleted')


class LikeView(generics.RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsBuyer, ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        like = Like.objects.filter(user=self.request.user, product=instance)
        if like:
            return Response("Like was already created")
        else:
            Like.objects.create(user=self.request.user, product=instance)
            return Response("Like created")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        like = Like.objects.filter(user=self.request.user, product=instance)
        if like:
            like.delete()
            return Response("Like is deleted")
        else:
            return Response("No Like")
