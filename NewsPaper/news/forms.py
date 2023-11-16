from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category


class NewsForm(forms.ModelForm):
    postCategory = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'postCategory']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        name = cleaned_data.get("title")

        if name == description:
            raise ValidationError(
                "Текст новости не должен состоять только из названия."
            )


class ArticleForm(forms.ModelForm):
    postCategory = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'postCategory']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        name = cleaned_data.get("title")

        if name == description:
            raise ValidationError(
                "Текст статьи не должен состоять только из названия."
            )
