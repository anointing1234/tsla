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
from accounts.models import ForexPlan,PaymentGateway,DepositTransaction,WalletAddress,Users_Investment,WithdrawTransaction,Balance,Order, Trade
from django.db.models import Sum,Q



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




def signup_view(request):
    return render(request,'forms/signup.html') 


def login_view(request):
    return render(request,'forms/login.html') 

def dash(request):
    try:
        balance = Balance.objects.get(user=request.user)
    except Balance.DoesNotExist:
        balance = None

    invested_amount = balance.invested_amount if balance else 0

    # 1. Matching plan
    matching_plans = ForexPlan.objects.filter(
        min_amount__lte=invested_amount
    ).filter(
        Q(max_amount__gte=invested_amount) | Q(max_amount__isnull=True)
    ).order_by("min_amount")
    account_plan = matching_plans.first()

    # 2. User investment totals
    if request.user.is_authenticated:
        plan = Users_Investment.objects.filter(user=request.user).order_by("-start_date")
        total_investment = (
            Users_Investment.objects.filter(user=request.user).aggregate(total=Sum("total"))["total"]
            or Decimal("0.00")
        )
    else:
        plan, total_investment = [], Decimal("0.00")

    # 3. Trading data (only current user!)
    buy_orders = Order.objects.filter(user=request.user, order_type="buy").order_by("-created_at")[:10]
    sell_orders = Order.objects.filter(user=request.user, order_type="sell").order_by("-created_at")[:10]
    recent_trades = Trade.objects.filter(buy_order__user=request.user).order_by("-timestamp")[:15]

    # 4. Trade summary
    estimated_total = trading_fee = net_amount = Decimal("0.00")
    fee_rate = Decimal("0.001")

    if request.method == "POST":
        try:
            amount = Decimal(request.POST.get("amount", "0"))
            price = Decimal(request.POST.get("price", "0"))
            estimated_total = amount * price
            trading_fee = estimated_total * fee_rate
            net_amount = estimated_total + trading_fee
        except Exception as e:
            print("❌ Error calculating trade summary:", e)

    return render(
        request,
        "dashboard/pages/index.html",
        {
            "account_plan": account_plan,
            "total_investment": total_investment,
            "plans": plan,
            "balance": balance,
            "buy_orders": buy_orders,
            "sell_orders": sell_orders,
            "recent_trades": recent_trades,
            "estimated_total": estimated_total,
            "trading_fee": trading_fee,
            "net_amount": net_amount,
            "fee_rate": fee_rate * 100,
        },
    )


def profile_view(request):
    return render(request,"dashboard/pages/profile.html")    

def referals(request):
    return render(request,'dashboard/pages/referrals.html')   

def Deposit_view(request):
    payment_gateways = PaymentGateway.objects.all()
    return render(request,'dashboard/pages/Deposit.html',{"payment_gateways": payment_gateways})  


def purchase_plan(request):
    plans = ForexPlan.objects.all() 
    return render(request,'dashboard/pages/purchase_plan.html',{'plans': plans})            

def view_plans(request):
    purchased_plans = Users_Investment.objects.filter(user=request.user).order_by('-start_date')
    return render(request,'dashboard/pages/view_plan.html',{'purchased_plans': purchased_plans})            

def withdraw_view(request):
    wallet_addresses = WalletAddress.objects.filter(user=request.user)
    return render(request,'dashboard/pages/withdraw.html', {'wallet_addresses': wallet_addresses})

def history(request):
    deposits = DepositTransaction.objects.filter(user=request.user).order_by("-date") 
    withdrawals = WithdrawTransaction.objects.filter(user=request.user)
    context = {
        'deposits': deposits,
        'withdrawals': withdrawals
    }
    return render(request,'dashboard/pages/history.html',context)

def first_view(request):
   return render(request,'dashboard/first_page.html')





def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)









