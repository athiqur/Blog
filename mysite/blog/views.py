from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(queryset, page, per_page):
    paginator = Paginator(queryset, per_page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return posts


def post_list(request):
    posts = paginate(Post.published.all(), request.Get.get("page"), 3)
    return render(
        request,
        "blog/post/list.html",
        {"page": request.Get.get("page"), "posts": posts},
    )


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post,
        slug=post_slug,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})
