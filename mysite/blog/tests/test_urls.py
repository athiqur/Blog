from django.test import SimpleTestCase
from blog.tests.test_modelmixintestcase import ModelMixinTestCase
from django.urls import resolve, reverse
from blog.views import (
    PostListView,
    PostShareView,
    PostListTagView,
    post_search,
)


class TestUrls(ModelMixinTestCase, SimpleTestCase):
    def test_post_list_url_is_resolved(self):
        self.assertEquals(
            resolve(reverse("blog:post_list")).func.view_class, PostListView
        )

    def test_post_share_url_is_resolved(self):
        self.assertEquals(
            resolve(
                reverse("blog:post_share", args=[self.published_post.id])
            ).func.view_class,
            PostShareView,
        )

    def test_post_list_by_tag_is_resolved(self):
        self.published_post.tags.add("test")
        recent_tag = self.published_post.tags.first()
        self.assertEquals(
            resolve(
                reverse("blog:post_list_by_tag", args=[recent_tag.slug])
            ).func.view_class,
            PostListTagView,
        )

    def test_post_search_url_is_resolved(self):
        self.assertEquals(
            resolve(reverse("blog:post_search")).func, post_search
        )
