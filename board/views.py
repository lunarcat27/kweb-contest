import math

from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .forms import *
from .models import *

def index(req):
    pass

def sign_up(req):
    pass

def sign_in(req):
    pass

def sign_out(req):
    pass

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