from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # указание на пользователя
    rating = models.SmallIntegerField(default=0)  # рейтинг пользователя

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')
        commentRat = self.user.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')
        compostRat = Post.objects.filter(author=self).aggregate(commentRating2=Sum('rating'))
        c2Rat = 0
        c2Rat += compostRat.get('commentRating2')
        self.rating = pRat * 3 + cRat + c2Rat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)  # категория


class Post(models.Model):
    # связь с моделью автор
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    # выбор статья или новость
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    post_type = models.CharField(choices=CATEGORY_CHOICES, max_length=2, default=ARTICLE)
    # автоматически добавляемая дата и время создания;
    dateCreation = models.DateTimeField(auto_now_add=True)
    # связь с моделью Category (с PostCategory);
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    # заголовок статьи/новости
    title = models.CharField(max_length=128)
    # текст статьи/новости
    text = models.TextField()
    # рейтинг статьи/новости
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        # превью статьи на 124 символа
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
