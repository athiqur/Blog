from blog.tests.test_modelmixintestcase import ModelMixinTestCase
from django.test import TestCase
from django.urls import reverse


class TestListView(ModelMixinTestCase, TestCase):
    def test_list_view_uses_correct_template(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertTemplateUsed(response, "blog/post/list.html")
