from django.test import TestCase
from blog.templatetags import blog_tags
from blog.models import Post, Comment
from blog.tests.test_modelmixintestcase import ModelMixinTestCase


class TestCustomTemplateTags(ModelMixinTestCase, TestCase):
    def test_total_post_returns_total_number_of_posts(self):
        self.assertEqual(blog_tags.total_posts(), 1)

    def test_latest_post_post_tag(self):
        post = Post.objects.create(
            title="latest",
            author=self.user,
            body="Testing Published",
            status="published",
            slug="published",
        )
        self.assertEquals(
            post.title,
            blog_tags.show_latest_posts()["latest_posts"].first().title,
        )
