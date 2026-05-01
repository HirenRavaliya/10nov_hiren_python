from django import forms
from .models import Post, Comment, Tag


class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        help_text='Enter tags separated by commas (e.g., python, django, web)',
        widget=forms.TextInput(attrs={'placeholder': 'python, django, web...'}),
        label='Tags',
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'cover_image', 'category', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15, 'class': 'post-content-editor'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            existing_tags = ', '.join(tag.name for tag in self.instance.tags.all())
            self.fields['tags_input'].initial = existing_tags

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            tags_data = self.cleaned_data.get('tags_input', '')
            instance.tags.clear()
            if tags_data:
                for tag_name in [t.strip() for t in tags_data.split(',') if t.strip()]:
                    tag, _ = Tag.objects.get_or_create(name__iexact=tag_name,
                                                       defaults={'name': tag_name})
                    instance.tags.add(tag)
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your thoughts...',
            }),
        }
        labels = {
            'content': '',
        }
