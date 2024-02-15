from datetime import datetime

from .serializers import ProductSerializer
from .models import Product
from .permissions import IsSellerOfProduct

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ProductCreateApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "podcategory", "user", "price", "available"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price"]
    permission_classes = [
        AllowAny,
    ]

    def get_queryset(self):
        query = self.request.query_params.get("search", "")
        min_price = self.request.query_params.get("min_price", None)
        max_price = self.request.query_params.get("max_price", None)
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)

        products = Product.objects.filter(name__icontains=query)

        if min_price is not None:
            products = products.filter(price__gte=min_price)

        if max_price is not None:
            products = products.filter(price__lte=max_price)

        if start_date is not None:
            products = products.filter(created__gte=start_date)

        if end_date is not None:
            products = products.filter(created__lte=end_date)

        return products

    # def get(self, request):
    #     products = request.user.store.products.all()
    #     srz_data = self.serializer_class(instance=products, many=True)
    #     return Response(data=srz_data.data, status=status.HTTP_200_OK)



# Представление для получения деталей, обновления и удаления продукта
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
        IsSellerOfProduct,]