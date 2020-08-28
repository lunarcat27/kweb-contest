import math

from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .forms import *
from .models import *

def index(req):
    return render(req, 'index.html')

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

def category_view_head(req):
    pass

def category_view(req):
    pass

def create_category(req):
    pass

def delete_category(req):
    pass

def get_article(req):
    pass

def compose_article(req):
    pass

def edit_article(req):
    pass

def delete_article(req):
    pass

def compose_comment(req):
    pass

def delete_comment(req):
    pass

def like(req):
    pass

def profile_index(req):
    pass

def profile_articles(req):
    pass