from .models import Comment
from django import forms

# to publish from front end
from .models import Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)



# for users to post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'status', 'likes', 'slug']

    featured_image = forms.ImageField(label='Featured Image', required=False)