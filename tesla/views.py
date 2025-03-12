from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils.html import strip_tags
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
import json
from django.contrib.auth.hashers import make_password,check_password
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
import os
from django.conf import settings
import shutil
from requests.exceptions import ConnectionError
import requests 
from django.contrib.auth.decorators import login_required
# from accounts.models import Transaction,Card
from django.db.models import Sum
# from accounts.models import ForexPlan


def home_view(request):
    return render(request,'home/index.html')


def faQ_view(request):
    return render(request,'home/faQ.html')


def contact_view(request):
    return render(request,'home/contact.html')


def academic_view(request):
    return render(request,'home/academic.html')


def about_view(request):
    return render(request,'home/about.html')


def awards_view(request):
    return render(request,'home/awards.html')


def affilate_view(request):
    return render(request,'home/affilate.html')


def news_view(request):
    API_KEY = "eaaef78551304676a82a67da78a00412"  # Replace with your actual API key
    url = f"https://newsapi.org/v2/everything?q=cryptocurrency&apiKey={API_KEY}"
    
    try:
        response = requests.get(url)
        news_data = response.json()
        
        # Fetch top 10 articles, but filter out those without images
        articles = [
            article for article in news_data.get("articles", []) 
            if article.get("urlToImage")  # Only include articles with an image
        ][:10]  # Limit to 10 articles
    except Exception as e:
        articles = []

    return render(request, 'home/news.html', {"articles": articles})

def tesla_cars_view(request):
    return render(request,'home/tesla_cars.html')
   





