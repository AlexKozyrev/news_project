from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (NewsList, PostDetail, NewsSearch, NewsCreate, NewsDelete, NewsUpdate, ArticleCreate, ArticleUpdate,
                    ArticleDelete, CategoryListView, subscribe, unsubscribe, categories)

urlpatterns = [
    path('', cache_page(60)(NewsList.as_view()), name='main_page'),
    path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
    path('subscriptions/', categories, name='subscriptions'),
]
