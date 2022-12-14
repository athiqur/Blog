from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, FormView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import TrigramSimilarity


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


class PostListTagView(ListView):
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

    def dispatch(self, request, *args, **kwargs):
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get("tag_slug"))
        return super().dispatch(request, args, kwargs)

    def get_queryset(self):
        return Post.published.filter(tags__in=[self.tag])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["tag"] = self.tag
        return data


@require_http_methods(["POST"])
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    comment_form = CommentForm(data=request.POST or None)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.save()
        messages.success(request, message="Comment added successfully")
        return redirect(
            "blog:post_detail",
            post.publish.year,
            post.publish.month,
            post.publish.day,
            post.slug,
        )

    return render(
        request,
        "blog/post/detail.html",
        {
            "comment_form": comment_form,
        },
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
    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comment_form": CommentForm,
            "similar_posts": post.get_top_four_similar_posts(),
        },
    )


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data["query"]
        results = Post.published.annotate(
            search=SearchVector("title", "body"),
        ).filter(search=query)
    return render(
        request,
        "blog/post/search.html",
        {"form": form, "query": query, "results": results},
    )


class PostShareView(SuccessMessageMixin, FormView):
    form_class = EmailPostForm
    template_name = "blog/post/share.html"
    success_url = reverse_lazy("blog:post_list")
    success_message = "mail sent"

    def dispatch(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(
            Post, id=self.kwargs.get("post_id")
        )
        return super().dispatch(request, args, kwargs)

    def form_valid(self, form):
        self.send_mail(form.cleaned_data)
        return super(PostShareView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.post_object
        return context

    def send_mail(self, valid_data):
        post_url = self.request.build_absolute_uri(
            self.post_object.get_absolute_url()
        )
        send_mail(
            message=f"Read {self.post_object.title} at { post_url }\n\n"
            f"{valid_data['from_name']}'s message: {valid_data['share_message']}",
            from_email=valid_data["from_email"],
            subject=f"{valid_data['from_name']} recommends you read {self.post_object.title}",
            recipient_list=[valid_data["to_email"]],
        )
