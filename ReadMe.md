## Create Example Posts through shell:
You can create example posts using Django's shell or through a management command. Here, I'll demonstrate using the Django shell:

Start the Django shell:

`python manage.py shell`

Inside the shell, create example posts:
```python
from blog.models import Post, Tag

# Assuming tags already exist, replace 'Technology' and 'Programming' with existing tag names
tag1 = Tag.objects.get_or_create(name='Technology')[0]
tag2 = Tag.objects.get_or_create(name='Programming')[0]

# Create example posts with tags
post1 = Post.objects.create(title='Example Post 1', content='Content of Example Post 1')
post1.tags.add(tag1)

post2 = Post.objects.create(title='Example Post 2', content='Content of Example Post 2')
post2.tags.add(tag2)
Exit the Django shell when you're done:

exit()
```
## Start the Server:

Apply initial migrations to set up your database schema:

`python manage.py makemigrations`

`python manage.py migrate`

Ensure your development server is running:

`python manage.py runserver`

## Superuser already set:
I have a superuser already set, you can log in to the admin site at http://127.0.0.1:8000/admin/

username: NavSanya

password: root

## Testing and Debugging:
Use Django's testing framework 
`python manage.py test`

## Access Posts via URLs:

- **List of all posts:** http://127.0.0.1:8000/blog/
- **Create a new post:** http://127.0.0.1:8000/blog/create/
- **Update a post (replace `<pk>` with post ID):** http://127.0.0.1:8000/blog/update/`<pk>`/
- **Filter posts by tags:** http://127.0.0.1:8000/blog/filter/?tags=Technology
- **Search posts by tag (replace `<tag_name>` with tag name):** http://127.0.0.1:8000/blog/search/<tag_name>/
- **View popular tags:** http://127.0.0.1:8000/blog/popular/


### Feel free to adjust the instructions or URLs as per your specific project requirements. If you have any more details to add or need further clarification, let me know!
