from rest_framework.response import Response
from .serializers import ProductSerializer, RecallSerializer
from .models import Product, Recall
from rest_framework.viewsets import GenericViewSet


from .serializers import ProductSerializer, ProductDetailSerializer
from .permissions import IsSellerOfProduct, IsAdminOrOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
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


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "podcategory", "user", "price", "available"]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "price"]
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        query = self.request.query_params.get("search", "")
        min_price = self.request.query_params.get("min_price", None)
        max_price = self.request.query_params.get("max_price", None)
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)

        products = Product.objects.filter(title__icontains=query)

        if min_price is not None:
            products = products.filter(price__gte=min_price)

        if max_price is not None:
            products = products.filter(price__lte=max_price)

        if start_date is not None:
            products = products.filter(created__gte=start_date)

        if end_date is not None:
            products = products.filter(created__lte=end_date)

        return products


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly, ]


class RecallListApiView(ListAPIView):
    serializer_class = RecallSerializer

    def get_queryset(self):
        queryset = Recall.objects.filter(product=self.kwargs['pk'])
        return queryset


class RecallViewSet(GenericViewSet):
    queryset = Recall.objects.all()
    serializer_class = RecallSerializer

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
