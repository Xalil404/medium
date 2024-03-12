from . import views
from django.urls import path

urlpatterns = [

    path("", views.landing_page, name='landing_page'),
    path('about/', views.about, name='about'),
    path('write/', views.write, name='write'),
    path('profile/', views.profile, name='profile'),
    path("PostList", views.PostList.as_view(), name="read"),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]