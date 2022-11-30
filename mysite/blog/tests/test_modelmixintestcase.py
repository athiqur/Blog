from django.test import TestCase
from blog.models import Post
from django.contrib.auth.models import User


class ModelMixinTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="athiqur",
            password="123",
        )

        self.draft_post = Post.objects.create(
            title="Draft",
            author=self.user,
            body="Testing Draft",
            status="draft",
        )
        self.published_post = Post.objects.create(
            title="Published",
            author=self.user,
            body="Testing Published",
            status="published",
<<<<<<< HEAD
=======
            slug="published",
>>>>>>> 7b3ab53 (Create detail view)
        )
