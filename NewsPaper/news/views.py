from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post
from .filters import NewsFilter
from .forms import NewsForm, ArticleForm


class NewsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsSearch(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = NewsForm
    template_name = 'news_edit.html'
    queryset = Post.objects.filter(post_type='NW')


class ArticleUpdate(UpdateView):
    form_class = ArticleForm
    template_name = 'article_edit.html'
    queryset = Post.objects.filter(post_type='AR')


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('main_page')

    def get_queryset(self):
        return super().get_queryset().filter(post_type='NW')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('main_page')

    def get_queryset(self):
        return super().get_queryset().filter(post_type='AR')
