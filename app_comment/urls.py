from django.urls import path, include

from .views import (CreateCommentView, CommentListView,
CommentDeleteApiView,
CommentDetailView,
ProductCommentsApiView
)


urlpatterns = [
    path("list/comment/", CommentListView.as_view(), name="list_of_comment"),
    path("product/comment/<int:product_id>/", ProductCommentsApiView.as_view(), name='комментарии определеного продукта'),
    path("create/comment/", CreateCommentView.as_view(), name="create_comment"),
    path("delete/comment/<int:pk>/", CommentDeleteApiView.as_view(), name='delete_comments'),
    path('detal/comment/<int:id>/', CommentDetailView.as_view()),
]