from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.validators import MinValueValidator
from django.urls import reverse


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
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name

    def get_category(self):
        return self.name


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
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
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

    def __str__(self):
        return f'{self.title}: {self.preview()[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            cache.delete(f'news-{self.pk}')
        except:
            print('not-work')




class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.contributable_attrs.name


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
