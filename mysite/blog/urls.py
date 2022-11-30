from django.urls import path
from . import views

app_name = "blog"
<<<<<<< HEAD
urlpatterns = [
    path("", views.post_list, name="post_list"),
=======

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post_slug>/",
        views.post_detail,
        name="post_detail",
    ),
>>>>>>> 7b3ab53 (Create detail view)
]
