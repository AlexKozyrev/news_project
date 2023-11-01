from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        name = cleaned_data.get("title")

        if name == description:
            raise ValidationError(
                "Текст новости не должен состоять только из названия."
            )


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        name = cleaned_data.get("title")

        if name == description:
            raise ValidationError(
                "Текст статьи не должен состоять только из названия."
            )
