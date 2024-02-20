from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductDetailView, ProductListApiView, ProductCreateApiView, ProductsByCategoryApiView, ProductsByPodCategoryApiView,RecallListApiView,RecallViewSet

router = DefaultRouter()
router.register('recall', RecallViewSet, basename='recall')


urlpatterns = [
    path('categories/<int:category_id>/products/', ProductsByCategoryApiView.as_view(), name='products_by_category'),
    path('podcategory/<int:podcategory_id>/products/', ProductsByPodCategoryApiView.as_view(), name='products_by_podcategory'),
    path("product/list/", ProductListApiView.as_view(), name="product-list"),
    path('product/create/', ProductCreateApiView.as_view(), name='product-create'),
    path("product/detail/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("like/<int:pk>/", LikeView.as_view(), name="like"),
    path('recall-list/<int:pk>/', RecallListApiView.as_view(), name='recall-list'),
    path('', include(router.urls)),
]

