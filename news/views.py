from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from core.views import staff_required

from .forms import NewsArticleForm
from .models import NewsArticle


def articles_visible_to(user):
    articles = NewsArticle.objects.select_related("author")
    if not user.is_authenticated or not user.is_staff:
        articles = articles.filter(visibility=NewsArticle.Visibility.SURVIVORS)
    return articles


def news_list(request):
    return render(
        request,
        "news/article_list.html",
        {"articles": articles_visible_to(request.user)},
    )


def news_detail(request, pk):
    article = get_object_or_404(articles_visible_to(request.user), pk=pk)
    return render(request, "news/article_detail.html", {"article": article})


@staff_required
def news_create(request):
    form = NewsArticleForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Новостная статья опубликована.")
        return redirect(article)
    return render(
        request,
        "news/article_form.html",
        {"form": form, "page_title": "Создать новостную статью"},
    )


@staff_required
def news_edit(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    form = NewsArticleForm(
        request.POST or None,
        request.FILES or None,
        instance=article,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Новостная статья обновлена.")
        return redirect(article)
    return render(
        request,
        "news/article_form.html",
        {
            "form": form,
            "article": article,
            "page_title": "Редактировать новостную статью",
        },
    )


@staff_required
def news_delete(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    if request.method == "POST":
        article.delete()
        messages.success(request, "Новостная статья удалена.")
        return redirect("news_manage")
    return render(
        request,
        "news/article_confirm_delete.html",
        {"article": article},
    )


@staff_required
def news_manage(request):
    articles = NewsArticle.objects.select_related("author")
    return render(request, "news/article_manage.html", {"articles": articles})
