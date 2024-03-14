from .models import Comment
from django import forms

# to publish from front end
from .models import Post
from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


# for users to post from the write post page
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'featured_image', 'excerpt', 'content']
        exclude = ['author', 'status', 'likes', 'slug']
        widgets = {
            'content': SummernoteWidget(),  # Use SummernoteWidget for the content field
        }

    featured_image = forms.ImageField(label='Featured Image', required=False)