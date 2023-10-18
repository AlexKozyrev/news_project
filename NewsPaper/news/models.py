from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # указание на пользователя
    rating = models.IntegerField()  # рейтинг пользователя

    def __init__(self):  # добавил по совету среды разработки
        super().__init__()
        self.comment_set = None
        self.post_set = None

    def update_rating(self):  # Вычисление рейтинга автора
        self.rating = self.post_set.aggregate(models.Sum('rating'))['rating__sum'] * 3
        self.rating += self.comment_set.aggregate(models.Sum('rating'))['rating__sum']
        self.rating += self.comment_set.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum']
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  # категория


class Post(models.Model):
    # связь с моделью автор
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # выбор статья или новость
    post_type = models.CharField(choices=[('article', 'Статья'), ('news', 'Новость')], max_length=8)
    # автоматически добавляемая дата и время создания;
    created_at = models.DateTimeField(auto_now_add=True)
    # связь с моделью Category (с PostCategory);
    categories = models.ManyToManyField(Category, through='PostCategory')
    # заголовок статьи/новости
    title = models.CharField(max_length=255)
    # текст статьи/новости
    text = models.TextField()
    # рейтинг статьи/новости
    rating = models.IntegerField()

    def preview(self):
        # превью статьи на 124 символа
        return self.text[:124] + ' ...'


class PostCategory(models.Model):
    # связь «один ко многим» с моделью Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь «один ко многим» с моделью Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    # связь «один ко многим» с моделью Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь «один ко многим» со встроенной моделью User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
