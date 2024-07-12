# blogs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('update/<int:pk>/', views.update_post, name='update_post'),
    path('filter/', views.filter_posts_by_tags, name='filter_posts_by_tags'),
    path('search/<str:tag_name>/', views.search_posts_by_tag, name='search_posts_by_tag'),
    path('popular/', views.popular_tags, name='popular_tags'),
]