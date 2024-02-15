from django.urls import path
from .views import ProductDetailView, ProductListApiView, ProductCreateApiView

urlpatterns = [

    path("product/list/", ProductListApiView.as_view(), name="product-list"),
    path('product/create/', ProductCreateApiView.as_view(), name='product-create'),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
]

