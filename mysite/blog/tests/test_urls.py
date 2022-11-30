from django.test import SimpleTestCase
from blog.tests.test_modelmixintestcase import ModelMixinTestCase
from django.urls import resolve, reverse
from blog.views import post_list


class TestUrls(ModelMixinTestCase, SimpleTestCase):
    def test_post_list_url_is_resolved(self):
        self.assertEquals(resolve(reverse("blog:post_list")).func, post_list)
