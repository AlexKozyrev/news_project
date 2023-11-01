from django.urls import path

from .views import (NewsList, PostDetail, NewsSearch, NewsCreate, NewsDelete, NewsUpdate, ArticleCreate, ArticleUpdate,
                    ArticleDelete)

urlpatterns = [
   path('', NewsList.as_view(), name='main_page'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', NewsSearch.as_view()),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view()),
   path('news/<int:pk>/delete/', NewsDelete.as_view()),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view()),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view())
]
