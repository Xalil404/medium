from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm


from django.shortcuts import render, redirect
from django.utils.text import slugify
from .forms import PostForm
from .models import STATUS
from django.contrib.auth.decorators import login_required


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )
    
    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    


def about(request):
    return render(request, 'about.html')


def landing_page(request):
    # Retrieve the six most recent posts
    recent_posts = Post.objects.filter(status=1).order_by('-created_on')[:6]
    return render(request, 'landing_page.html', {'recent_posts': recent_posts})


@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(author=user)
    return render(request, 'profile.html', {'posts': posts, 'user': user})


@login_required
def write(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # Set status to "published"
            post.status = STATUS[1][0]
            
            # Generate unique slug based on the title
            slug = slugify(post.title)
            unique_slug = slug
            counter = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{slug}-{counter}'
                counter += 1
            post.slug = unique_slug
            
            post.save()
            return redirect('post_detail', slug=post.slug)  # Redirect to post_detail view after successful submission
    else:
        form = PostForm()
    return render(request, 'write.html', {'form': form})

