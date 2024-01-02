from django.contrib import admin
from .models import Post, Category


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'dateCreation', 'rating', 'display_categories']

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.postCategory.all()])

    display_categories.short_description = 'Categories'


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
