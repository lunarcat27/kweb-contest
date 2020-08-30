import math

from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .forms import *
from .models import *

def index(req):
    return render(req, 'index.html', {'form': CategoryForm(), 'categories': Category.objects.all().filter(is_deleted = False),})

def sign_up(req):
    if req.user.is_authenticated:
        return HttpResponse(status = 404)
    if req.method == 'GET':
        return sign_up_form(req)
    if req.method == 'POST':
        return sign_up_post(req)
    return HttpResponse(status = 404)

def sign_up_form(req):
    return render(req, 'auth/sign_up.html', {'form': SignUpForm(),})

def sign_up_post(req):
    form = SignUpForm(req.POST)
    if not form.is_valid():
        return HttpResponse(status = 400)

    user = User.objects.create_user(
        username = form.cleaned_data['username'],
        password = form.cleaned_data['password'],
        email = form.cleaned_data['email'],
    )
    user.save()

    return redirect('sign_in')

def sign_in(req):
    if req.user.is_authenticated:
        return HttpResponse(status = 404)
    if req.method == 'GET':
        return sign_in_form(req)
    if req.method == 'POST':
        return sign_in_post(req)
    return HttpResponse(status = 404)

def sign_in_form(req):
    return render(req, 'auth/sign_in.html', {'form': SignInForm(),})

def sign_in_post(req):
    form = SignInForm(req.POST)
    if not form.is_valid():
        return HttpResponse(status = 400)

    user = authenticate(
        username = form.cleaned_data['username'],
        password = form.cleaned_data['password'],
    )

    if user:
        login(req, user)
        return redirect('index')
    else:
        return HttpResponse(status = 401)

def sign_out(req):
    logout(req)
    return redirect('index')

def category_view_head(req, category_id):
    return redirect('category_view', category_id = category_id, page = 1)

def category_view(req, category_id, page):
    article_list = Article.objects.all().filter(is_deleted = False).filter(category = category_id).order_by('-id')

    COUNT = 5
    start_index = (page - 1) * COUNT
    end_index = page * COUNT

    page_count = math.ceil(len(article_list) / COUNT)

    return render(req, 'articles/index.html', {
        'page': page,
        'category': Category.objects.get(pk = category_id),
        'articles': article_list[start_index:end_index],
        'has_prev': page > 1,
        'has_next': page < page_count,
    })

def create_category(req):
    if not req.user.is_authenticated:
        return HttpResponse(status = 404)
    if req.method == 'POST':
        return create_category_post(req)
    return HttpResponse(status = 404)

def create_category_post(req):
    form = CategoryForm(req.POST)
    if not form.is_valid():
        return HttpResponse(status = 400)

    category = Category.objects.create(
        name = form.cleaned_data['name'],
        creator = req.user,
    )
    category.save()

    return redirect('category_view_head', category_id = category.id)

def delete_category(req, category_id):
    if not req.user.is_authenticated:
        return HttpResponse(status = 404)

    category = get_object_or_404(Category, id = category_id, is_deleted = False, creator = req.user)

    articles = Article.objects.all().filter(is_deleted = False).filter(category = category_id)

    for article in articles:
        article.is_deleted = True
        article.save()

    category.is_deleted = True
    category.save()

    return redirect('index')

def get_article(req, article_id):
    article = get_object_or_404(Article, id = article_id, is_deleted = False)
    comments = Comment.objects.all().filter(is_deleted = False).filter(article = article_id).order_by('-id')
    likes = article.like.all()
    isLiked = False

    for user in likes:
        if user == req.user:
            isLiked = True
            break

    return render(req, 'articles/details.html', {
        'article': article,
        'comments': comments,
        'comments_count': comments.count(),
        'likes_count': likes.count(),
        'liked': isLiked,
        'form': CommentForm(),
    })

def compose_article(req, category_id):
    if not req.user.is_authenticated:
        return HttpResponse(status = 404)
    if req.method == 'GET':
        return compose_article_form(req)
    if req.method == 'POST':
        return compose_article_post(req, category_id)
    return HttpResponse(status = 404)

def compose_article_form(req):
    return render(req, 'articles/compose.html', {'form': ArticleForm(), 'is_compose': True})

def compose_article_post(req, category_id):
    form = ArticleForm(req.POST)
    if not form.is_valid():
        return HttpResponse(status = 400)

    article = Article.objects.create(
        title = form.cleaned_data['title'],
        content = form.cleaned_data['content'], 
        author = req.user,
        category = Category.objects.get(pk = category_id),
    )
    article.save()

    return redirect('get_article', article_id = article.id)

def edit_article(req, article_id):
    if not req.user.is_authenticated:
        return HttpResponse(status = 404)

    article = get_object_or_404(Article, id = article_id, is_deleted = False, author = req.user)

    if req.method == 'GET':
        return edit_article_form(req, article)
    if req.method == 'POST':
        return edit_article_post(req, article)
    return HttpResponse(status = 404)

def edit_article_form(req, article):
    return render(req, 'articles/compose.html', {
        'form': ArticleForm(initial = {
            'title': article.title,
            'content': article.content,
            }),
        'is_compose': False
        })

def edit_article_post(req, article):
    form = ArticleForm(req.POST)
    if not form.is_valid():
        return HttpResponse(status = 400)

    article.title = form.cleaned_data['title']
    article.content = form.cleaned_data['content']
    article.save()

    return redirect('get_article', article_id = article.id)

def delete_article(req, article_id):
    if not req.user.is_authenticated:
        return HttpResponse(status = 404)

    article = get_object_or_404(Article, id = article_id, is_deleted = False, author = req.user)

    article.is_deleted = True
    article.save()

    return redirect('category_view_head', category_id = article.category.pk)

def compose_comment(req, article_id):
    if not req.user.is_authenticated:
        return HttpResponse(status = 404)
    if req.method == 'POST':
        return compose_comment_post(req, article_id)
    return HttpResponse(status = 404)

def compose_comment_post(req, article_id):
    article = Article.objects.get(pk = article_id)

    if article.is_deleted == True:
        return HttpResponse(status = 404)

    form = CommentForm(req.POST)
    if not form.is_valid():
        return HttpResponse(status = 400)

    comment = Comment.objects.create(
        content = form.cleaned_data['content'],
        author = req.user,
        article = article,
    )
    comment.save()

    return redirect('get_article', article_id = article_id)

def delete_comment(req, comment_id):
    if not req.user.is_authenticated:
        return HttpResponse(status = 404)

    comment = get_object_or_404(Comment, id = comment_id, is_deleted = False, author = req.user)

    comment.is_deleted = True
    comment.save()

    return redirect('get_article', article_id = comment.article.pk)

def like(req, article_id):
    if not req.user.is_authenticated:
        return HttpResponse(status = 404)

    article = get_object_or_404(Article, id = article_id, is_deleted = False)
    likes = article.like.all()
    isLiked = False

    for user in likes:
        if user == req.user:
            isLiked = True
            break

    if isLiked:
        article.like.remove(req.user)
    else:
        article.like.add(req.user)

    return redirect('get_article', article_id = article_id)

def profile_index(req, username):
    return render(req, 'profile/index.html', {'profile_user': get_object_or_404(User, username = username),})

def profile_articles(req, username):
    user = get_object_or_404(User, username = username)
    return render(req, 'profile/articles.html', {
        'profile_user': user,
        'articles': Article.objects.all().filter(is_deleted = False)
        .filter(author = user.pk)
        .order_by('-id')
        })