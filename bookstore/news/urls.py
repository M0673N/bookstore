from django.urls import path

from . import views

urlpatterns = [
    path('news/', views.ListArticlesView.as_view(), name='news'),
    path('add-article/', views.AddArticleView.as_view(), name='add article'),
    path('article-details/<int:pk>', views.ArticleDetailsView.as_view(), name='article details'),
    path('edit-article/<int:pk>', views.EditArticleView.as_view(), name='edit article'),
    path('delete-article/<int:pk>', views.DeleteArticleView.as_view(), name='delete article'),
    path('comment-article/<int:pk>', views.CommentArticleView.as_view(), name='comment article'),
    path('delete-article-comment/<int:apk>/<int:cpk>', views.DeleteArticleCommentView.as_view(),
         name='delete article comment'),
]
