from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryListView,
    CategoryCreateApiView,
    CategoryDetailView,
    PodCategoryListView,
    PodCategoryCreateApiView,
    PodCategoryDetailView
)

# router = DefaultRouter()
# router.register(r"pod/category", PodCategoryViewSet, basename="PodCategory")


urlpatterns = [
    path("categories/list/", CategoryListView.as_view(), name="category-list"),
    path('categories/create/', CategoryCreateApiView.as_view(), name='category-create'),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    # path("", include(router.urls))
    path("pod/category/list/", PodCategoryListView.as_view(), name="PodCategory-list"),
    path('pod/category/create/', PodCategoryCreateApiView.as_view(), name='PodCategory-create'),
    path("pod/category/<int:pk>/", PodCategoryDetailView.as_view(), name="PodCategory-detail"),
]