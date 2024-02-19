from django.urls import path
from .views import LikeView, LikeDeleteApiView, LikeListApiView

urlpatterns = [
    path('create/', LikeView.as_view(), name='like-product-post'),
    path('delete/<int:pk>/', LikeDeleteApiView.as_view(), name='delete like'),
    path('list/', LikeListApiView.as_view(), name='list like'),
    # path('favorite/products/', FavoriteProductsView.as_view(), name='favorite-products'),
]