from django import forms
from .models import Post, Tag

class PostForm(forms.ModelForm):
    tags = forms.CharField(max_length=200, help_text="Enter tags separated by commas")

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def save(self, commit=True):
        post = super().save(commit=False)
        tag_names = self.cleaned_data['tags'].split(',')
        
        if commit:
            post.save()
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)
                    if created:
                        tag.usage_count += 1
                        tag.save()
        return post
