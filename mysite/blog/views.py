from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


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


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    form = get_forms_post_request_data_or_none(
        request.POST or None, EmailPostForm
    )
    if form.is_valid():
        send_email(request, post, form.cleaned_data)
    else:
        form = get_empty_form(EmailPostForm)
    return render(
        request,
        "blog/post/share.html",
        {
            "post": post,
            "form": form,
            "sent": form.is_valid(),
        },
    )


def get_forms_post_request_data_or_none(request, EmailPostForm):
    return EmailPostForm(request)


def get_empty_form(EmailPostForm):
    return EmailPostForm()


def send_email(request, post, cleaned_data):
    post_url = request.build_absolute_uri(post.get_absolute_url())
    subject = f"{cleaned_data['name']} recommends you read " f"{post.title}"
    message = (
        f"Read {post.title} at {post_url}\n\n"
        f"{cleaned_data['name']}'s comments: {cleaned_data['comments']}"
    )
    send_mail(subject, message, "athiqurking@gmail.com", [cleaned_data["to"]])
