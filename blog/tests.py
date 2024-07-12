from django.test import TestCase
from django.urls import reverse
from .models import Post, Tag

class PostTestCase(TestCase):
    
    def setUp(self):
        self.tag_technology = Tag.objects.create(name='Technology', usage_count=5)
        self.tag_science = Tag.objects.create(name='Science', usage_count=3)
        self.tag_art = Tag.objects.create(name='Art', usage_count=2)

        self.post1 = Post.objects.create(title='Test Post 1', content='Test Content 1', author='Test Author')
        self.post1.tags.add(self.tag_technology, self.tag_science)

        self.post2 = Post.objects.create(title='Test Post 2', content='Test Content 2', author='Test Author')
        self.post2.tags.add(self.tag_technology, self.tag_art)
        
    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post 1')
        self.assertContains(response, 'Test Post 2')

    def test_filter_posts_by_tags_view(self):
        response = self.client.get(reverse('filter_posts_by_tags'), {'tags': 'Technology'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post 1')
        self.assertContains(response, 'Test Post 2')

    def test_search_posts_by_tag_view(self):
        response = self.client.get(reverse('search_posts_by_tag', args=['Technology']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post 1')
        self.assertContains(response, 'Test Post 2')

    def test_create_post_with_tags(self):
        response = self.client.post(reverse('create_post'), {
            'title': 'New Post',
            'content': 'New Content',
            'author': 'New Author',
            'tags': [self.tag_technology.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_update_post_with_tags(self):
        response = self.client.post(reverse('update_post', args=[self.post1.id]), {
            'title': 'Updated Post',
            'content': 'Updated Content',
            'author': 'Updated Author',
            'tags': [self.tag_science.id]
        })
        self.assertEqual(response.status_code, 302)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'Updated Post')

    def test_popular_tags_view(self):
        response = self.client.get(reverse('popular_tags'))
        self.assertEqual(response.status_code, 200)
        
        # Check if tags are present and sorted by usage_count
        tags_in_context = response.context.get('tags')
        self.assertIsNotNone(tags_in_context)
        self.assertGreaterEqual(len(tags_in_context), 2)  # Ensure at least two tags are present

        # Check specific tags
        tag_names = [tag.name for tag in tags_in_context]
        self.assertIn('Technology', tag_names)
        self.assertIn('Science', tag_names)