# blogs/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Tag

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blogs/post_list.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag_names = request.POST.get('tags').split(',')

        post = Post.objects.create(title=title, content=content)
        
        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if tag_name:  # Ensure the tag is not empty
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)
                tag.usage_count += 1
                tag.save()
                
        return redirect('post_list')
    
    return render(request, 'blogs/create_post.html')

def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag_names = request.POST.get('tags').split(',')

        post.title = title
        post.content = content
        post.tags.clear()  # Clear existing tags

        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if tag_name:  # Ensure the tag is not empty
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)
                tag.usage_count += 1
                tag.save()

        post.save()
        return redirect('post_list')

    return render(request, 'blogs/update_post.html', {'post': post})

def filter_posts_by_tags(request):
    if request.method == 'GET':
        tags = request.GET.getlist('tags')  # Get list of tags from query parameters

        if tags:
            # Initialize a queryset with all posts
            filtered_posts = Post.objects.all()

            # Iterate through each tag and filter posts that contain any of the tags
            for tag in tags:
                filtered_posts = filtered_posts.filter(tags__name__icontains=tag)

            # Distinct to avoid duplicate posts
            filtered_posts = filtered_posts.distinct()

            return render(request, 'blogs/filtered_posts.html', {'posts': filtered_posts, 'tags': tags})
        else:
            # If no tags are selected, return all posts
            posts = Post.objects.all()
            return render(request, 'blogs/post_list.html', {'posts': posts})

    return render(request, 'blogs/post_list.html', {'posts': posts})

def search_posts_by_tag(request, tag_name):
    posts = Post.objects.filter(tags__name__icontains=tag_name)
    return render(request, 'blogs/search_results.html', {'posts': posts})
    
def popular_tags(request):
    tags = Tag.objects.order_by('-usage_count')[:3]  # Get top 3 tags by usage count

    return render(request, 'blogs/popular_tags.html', {'tags': tags})
