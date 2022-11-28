from blog.tests.test_modelmixintestcase import ModelMixinTestCase
from django.test import TestCase
from django.urls import reverse


class TestListView(ModelMixinTestCase, TestCase):
    def test_post_list_GET(self):
        template = self.client.get(reverse("blog:post_list"))
        self.assertTemplateUsed(template, "blog/post/list.html")
