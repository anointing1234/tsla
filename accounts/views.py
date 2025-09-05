from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from django.contrib.auth import login,authenticate,get_user_model 
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import logout as auth_logout,login as auth_login,authenticate
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password,check_password
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
import os
from email.mime.image import MIMEImage
from django.conf import settings
import shutil
from django.utils.timezone import now
from requests.exceptions import ConnectionError
import requests 
import uuid
from uuid import uuid4
# from accounts.form  
import traceback
import threading
# from .models import -
import random
from django.utils.crypto import get_random_string
from django.utils.timezone import now, timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from .models import Account 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from .models import  WalletAddress,PaymentGateway,DepositTransaction,WithdrawTransaction,Balance,TransactionCodes,Users_Investment,ForexPlan,BankWithdrawal
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

def register(request):
    if request.method == "POST":
        try:
            # If data is sent as JSON
            if request.content_type == "application/json":
                data = json.loads(request.body)
                email = data.get("email")
                password = data.get("password")
                confirm_password = data.get("confirmPassword")
                first_name = data.get("first_name")
                phone = data.get("phone")
                country = data.get("country")
                currency = data.get("currency")
                language = data.get("language")  # Optional, if applicable
            else:  # If form data is sent (multipart/form-data or application/x-www-form-urlencoded)
                email = request.POST.get("user[email]")
                password = request.POST.get("user[password]")
                confirm_password = request.POST.get("user[confirmPassword]")
                first_name = request.POST.get("user[first_name]")
                phone = request.POST.get("user[phone]")
                country = request.POST.get("user[country]")
                currency = request.POST.get("user[currency]")
                language = request.POST.get("user[language]")  # Optional, if provided

            # Validate required fields
            if not all([first_name,phone, email, country, currency, password, confirm_password]):
                return JsonResponse({'success': False, 'error': 'All fields are required!'})

            if password != confirm_password:
                return JsonResponse({'success': False, 'error': 'Passwords do not match!'})

            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'error': 'Email is already in use!'})

            # Create and save user with additional fields
            user = User.objects.create_user(email=email, password=password)
            user.fullname = first_name
            user.phone = phone
            user.country = country
            user.currency = currency
            # Optionally set language if your model has it
            if language:
                user.language = language
            user.save()

            # Log in the user
            login(request, user)

            # Prepare welcome email details
            subject = "Welcome to Tesla Legacy Capital Partners"
            # Plain text version
            message_text = (
                f"Dear {first_name},\n\n"
                "Welcome to Tesla Legacy Capital Partners! We are delighted to have you on board.\n\n"
                "Explore our platform and start your journey towards smarter investments.\n\n"
                "Best Regards,\n"
                "Tesla Legacy Capital Partners Team"
            )
            # HTML version (professional and well-formatted)
            message_html = f"""
                <html>
                  <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.5;">
                    <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd;">
                      <h2 style="color: #0072ff; text-align: center;">Welcome to Tesla Legacy Capital Partners</h2>
                      <p>Dear {first_name}</p>
                      <p>
                        Thank you for registering with <strong>Tesla Legacy Capital Partners</strong> – the leading trading platform in the USA.
                        We are excited to help you explore new financial opportunities and achieve your investment goals.
                      </p>
                      <p>
                        Your account has been successfully created. You can now log in and start exploring our features.
                      </p>
                      <p>
                        If you have any questions or need assistance, please feel free to contact our support team.
                      </p>
                      <p style="margin-top: 30px;">Best Regards,<br>
                         <em>Tesla Legacy Capital Partners Team</em>
                      </p>
                    </div>
                  </body>
                </html>
            """

            # Send welcome email to the registered user
            async_send_mail(
                subject,
                message_text,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=message_html,
                fail_silently=False,
            )


            return JsonResponse({'success': True, 'message': 'Registration successful! A welcome email has been sent.'})

        except Exception as e:
            # For debugging, you can log the traceback or error message
            error_message = f"Error: {str(e)}"
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': error_message})

    return render(request, 'forms/signup.html')



def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "message": "Login successful!"})
        else:
            return JsonResponse({"success": False, "message": "Invalid email or password. Please try again."})

    return render(request, "forms/login.html")










@csrf_exempt
def logout_view(request):
    """Logs out the user and redirects to the login page."""
    if request.method == "POST":
        auth_logout(request)
        request.session.flush()
        return redirect("home") 
    return redirect("home") 




def confirm_deposit_view(request, pk):
    deposit = get_object_or_404(DepositTransaction, pk=pk)
    
    # Fetch balance using the user from DepositTransaction
    balance = get_object_or_404(Balance, user=deposit.user)
    
    if deposit.status != "completed":
        deposit.status = "completed"
        deposit.save()
        
        # Update user balance
        balance.usdt_balance += deposit.amount 
        balance.invested_amount += deposit.amount 
        balance.save()

        messages.success(request, f"Deposit {deposit.tx_ref} has been confirmed successfully.")
        messages.success(request, f"Balance update for {deposit.user} has been credited successfully.")
    else:
        messages.warning(request, f"Deposit {deposit.tx_ref} is already confirmed.")

    return redirect("admin:accounts_deposittransaction_changelist")






def decline_deposit_view(request, pk):
    deposit = get_object_or_404(DepositTransaction, pk=pk)

    if deposit.status == "pending":
        deposit.status = "declined"
        deposit.save()
        messages.error(request, f"Deposit {deposit.tx_ref} has been declined.")
    else:
        messages.warning(request, f"Deposit {deposit.tx_ref} cannot be declined as it is already {deposit.status}.")

    return redirect("admin:app_deposittransaction_changelist")











def confirm_withdraw(request, withdraw_id):
    """Confirm a pending withdrawal."""
    withdrawal = get_object_or_404(WithdrawTransaction, pk=withdraw_id)
    if withdrawal.status == "pending":
        withdrawal.status = "completed"
        withdrawal.save()
        messages.success(request, f"Withdrawal {withdrawal.tx_ref} confirmed successfully!")
    else:
        messages.warning(request, "This withdrawal is not pending.")
    # Change 'withdrawtransaction_list' to the URL name where you list withdrawals.
    return redirect("admin:accounts_withdrawtransaction_changelist")

def decline_withdraw(request, withdraw_id):
    """Decline a pending withdrawal and refund the user."""
    withdrawal = get_object_or_404(WithdrawTransaction, pk=withdraw_id)
    if withdrawal.status == "pending":
        withdrawal.status = "failed"
        # Refund the user
        balance = Balance.objects.get(user=withdrawal.user)
        balance.usdt_balance += withdrawal.amount
        balance.save()
        withdrawal.save()
        messages.error(request, f"Withdrawal {withdrawal.tx_ref} declined and refunded!")
    else:
        messages.warning(request, "This withdrawal is not pending.")
    # Change 'withdrawtransaction_list' to the URL name where you list withdrawals.
    return redirect("admin:accounts_withdrawtransaction_changelist")








def verify_reset_code(request):
    if request.method == "POST":
        email = request.POST.get("email")
        reset_code = request.POST.get("reset_code")
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not all([email, reset_code, new_password, confirm_password]):
            messages.error(request, "All fields are required.")
            return render(request, "forms/reset_pass.html")  # No redirect!

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "forms/reset_pass.html")  # No redirect!

        try:
            user = User.objects.get(email=email)
            transaction_code = TransactionCodes.objects.get(user=user)
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
            return render(request, "forms/reset_pass.html")
        except TransactionCodes.DoesNotExist:
            messages.error(request, "Invalid reset code.")
            return render(request, "forms/reset_pass.html")

        # Ensure reset code is valid
        if (
            str(transaction_code.reset_code) != reset_code
            or transaction_code.reset_code_status != "active"
            or now() - transaction_code.reset_code_created_at > timedelta(minutes=20)
        ):
            messages.error(request, "Invalid or expired reset code.")
            return render(request, "forms/reset_pass.html")

        # Reset the password
        user.password = make_password(new_password)
        user.save()

        # Mark reset code as used
        transaction_code.reset_code_status = "used"
        transaction_code.save()

        messages.success(request, "Password reset successful. Please login.")
        return render(request, "forms/reset_pass.html")  # Render with messages

    return render(request, "forms/reset_pass.html")






def send_pass_views(request):
    return render(request,'forms/send_reset_pass.html')

def reset_pass(request):
    return render(request,'forms/reset_pass.html')



def send_reset_code(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = get_object_or_404(Account, email=email)  # Check if user exists
        
        # Generate a 6-digit reset code
        reset_code = str(random.randint(100000, 999999))

        # Fetch or create TransactionCodes for the user
        transaction_code, created = TransactionCodes.objects.get_or_create(user=user)

        # Update reset code details
        transaction_code.reset_code = reset_code
        transaction_code.reset_code_created_at = now()
        transaction_code.reset_code_status = "active"
        transaction_code.save()

        # Send reset code via email
        async_send_mail(
            "Password Reset Code",
            f"Your password reset code is: {reset_code}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )


        return JsonResponse({"success": True, "message": "Reset code sent to your email."})
    
    return JsonResponse({"success": False, "message": "Invalid request."})






def update_withdrawal_account(request):
    if request.method == "POST":
        user = request.user
        wallet_address = request.POST.get("wallet_address", "").strip()
        currency = request.POST.get("currency", "").strip()

        # Ensure required fields are filled
        if not wallet_address or not currency:
            messages.error(request, "Wallet address and currency are required.")
            return render(request, "dashboard/pages/profile.html")  # Redirect instead of render

        # Ensure valid currency selection
        valid_currencies = ["BTC", "ETH", "USDT_TRX", "USDT_ETH", "LTC", "TRX", "BCH"]
        if currency not in valid_currencies:
            messages.error(request, "Invalid currency selected.")
            return render(request, "dashboard/pages/profile.html")

        # Update or create wallet address
        wallet, created = WalletAddress.objects.update_or_create(
            user=user, currency=currency,
            defaults={"address": wallet_address}
        )

        if created:
            messages.success(request, "Withdrawal account added successfully!")
        else:
            messages.success(request, "Withdrawal account updated successfully!")

        return redirect("profile")  # Redirect after updating

    return render(request, "dashboard/pages/profile.html")











def update_password(request):
    if request.method == "POST":
        user = request.user
        current_password = request.POST.get("current_password", "").strip()
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        # Check if current password is correct
        if not check_password(current_password, user.password):
            messages.error(request, "Current password is incorrect!")
            return render(request, "dashboard/pages/profile.html")

        # Check if new password matches confirmation
        if new_password != confirm_password:
            messages.error(request, "New password and confirmation do not match!")
            return render(request, "dashboard/pages/profile.html")

        # Update password
        user.set_password(new_password)
        user.save()

        # Keep user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully!")
        return render(request, "dashboard/pages/profile.html")
    return render(request, "dashboard/pages/profile.html")






def update_profile(request):
    if request.method == "POST":
        user = request.user
        email = request.POST.get("email", "").strip()
        fullname = request.POST.get("fullname", "").strip()
        country = request.POST.get("country", "").strip()
        phone = request.POST.get("phone", "").strip()

        # Update user profile fields
        user.email = email
        user.fullname = fullname
        user.country = country
        user.phone = phone
        user.save()

        messages.success(request, "Profile updated successfully!")
        return render(request, "dashboard/pages/profile.html") # Change to your profile URL name

    return render(request, "dashboard/pages/profile.html")






def update_profile_picture(request):
    if request.method == "POST" and request.FILES.get("profile_picture"):
        user = request.user
        user.profile_picture = request.FILES["profile_picture"]
        user.save()
        messages.success(request, "Profile picture updated successfully!")
    else:
        messages.error(request, "No file selected. Please choose a valid image.")
    return render(request, "dashboard/pages/profile.html")





def deposit_funds(request):
    payment_gateways = PaymentGateway.objects.all()  # Fetch once to avoid repeated queries

    if request.method == "POST":
        user = request.user
        payment_method = request.POST.get("payment_method", "").strip()
        deposit_amount = request.POST.get("deposit_amount", "").strip()
        payment_screenshot = request.FILES.get("payment_screenshot")

        # Validate input fields
        if not payment_method or not deposit_amount or not payment_screenshot:
            messages.error(request, "All fields are required.")
            return render(request, "dashboard/pages/Deposit.html", {"payment_gateways": payment_gateways})

        # Validate deposit amount
        try:
            deposit_amount = float(deposit_amount)
            if deposit_amount <= 0:
                messages.error(request, "Deposit amount must be greater than zero.")
                return render(request, "dashboard/pages/Deposit.html", {"payment_gateways": payment_gateways})
        except ValueError:
            messages.error(request, "Invalid deposit amount format.")
            return render(request, "dashboard/pages/Deposit.html", {"payment_gateways": payment_gateways})

        # Fetch wallet address from PaymentGateway
        gateway = PaymentGateway.objects.filter(currency=payment_method).first()
        if not gateway:
            messages.error(request, f"No payment gateway found for {payment_method}.")
            return render(request, "dashboard/pages/Deposit.html", {"payment_gateways": payment_gateways})

        # Generate a unique transaction reference
        tx_ref = f"DEP-{uuid.uuid4().hex[:10].upper()}"

        # Save the deposit transaction
        DepositTransaction.objects.create(
            user=user,
            method=payment_method,
            amount=deposit_amount,
            tx_ref=tx_ref,
            screenshot=payment_screenshot,
            status="pending",
        )

        messages.success(request, "Deposit request submitted successfully!")

        # ✅ Use redirect to make messages persist
        return redirect("Deposit")  # Ensure 'deposit_page' is the correct URL name for the deposit page

    return render(request, "dashboard/pages/Deposit.html", {"payment_gateways": payment_gateways})






def purchase_plan_view(request):
    if request.method == "POST":
        plan_id = request.POST.get("plan_id")
        amount = request.POST.get("amount")

        if not plan_id or not amount:
            messages.error(request, "Invalid plan selection!")
            return redirect("purchase_plan")

        # Convert amount to Decimal
        amount = Decimal(amount)

        # Fetch the selected plan
        plan = get_object_or_404(ForexPlan, id=plan_id)

        # Validate investment amount
        if amount < plan.min_amount:
            messages.error(request, f"Investment amount must be at least ${plan.min_amount}!")
            return redirect("purchase_plan")
        if plan.max_amount is not None and amount > plan.max_amount:
            messages.error(request, f"Investment amount must be no more than ${plan.max_amount}!")
            return redirect("purchase_plan")

        # Check if user already has an active investment in this plan
        existing_plan = Users_Investment.objects.filter(user=request.user, plan=plan, status="active").exists()
        if existing_plan:
            messages.error(request, f"You already have an active '{plan.name}' plan. Wait until it expires before purchasing again.")
            return redirect("purchase_plan")

        # Get user's balance
        balance = Balance.objects.get(user=request.user)

        # Check if user has enough balance
        if balance.usdt_balance < amount:
            messages.error(request, "Insufficient balance to purchase this plan!")
            return redirect("purchase_plan")

        # Deduct the amount from user's balance
        balance.usdt_balance -= amount
        balance.save()

        # Calculate total profit for a 24-hour plan (entire profit realized in one cycle)
        total_profit = amount * (Decimal(plan.percentage) / Decimal(100))

        # Create investment entry without daily_income
        Users_Investment.objects.create(
            user=request.user,
            uniq_id=str(uuid.uuid4()),  # Unique ID for tracking
            plan=plan,
            profit=total_profit,
            total=amount + total_profit,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=1),  # 24-hour cycle
            status="active",
        )

        messages.success(request, f"Plan '{plan.name}' purchased successfully!")
      
    return redirect("purchase_plan")



def withdraw_funds(request):
    user = request.user
    balance = Balance.objects.get(user=user)

    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method."})

    withdraw_type = request.POST.get("withdraw_type")
    withdraw_amount_raw = request.POST.get("withdraw_amount")

    # Validate withdraw amount
    try:
        withdraw_amount = Decimal(withdraw_amount_raw)
        if withdraw_amount <= 0:
            return JsonResponse({"success": False, "message": "Amount must be greater than zero."})
    except Exception:
        return JsonResponse({"success": False, "message": "Invalid withdrawal amount."})

    # Common balance check
    if withdraw_amount > balance.usdt_balance:
        return JsonResponse({"success": False, "message": "Insufficient balance."})

    if withdraw_type == "crypto":
        withdraw_currency = request.POST.get("withdraw_currency")
        withdraw_address  = request.POST.get("withdraw_address")

        if not withdraw_currency or not withdraw_address:
            return JsonResponse({
                "success": False,
                "message": "Currency and address required for crypto withdrawal."
            })

        # Deduct from USDT balance
        balance.usdt_balance -= withdraw_amount
        balance.save()

        # Create crypto withdrawal transaction
        WithdrawTransaction.objects.create(
            user=user,
            currency=withdraw_currency,
            withdraw_address=withdraw_address,
            amount=withdraw_amount,
            tx_ref=str(uuid4()),
            status="pending",
        )

    elif withdraw_type == "bank":
        bank_name     = request.POST.get("bank_name")
        fullname      = request.POST.get("account_name")
        swift_code    = request.POST.get("swift_code")
        currency      = request.POST.get("currency")
        account_number= request.POST.get("account_number")

        # Validate all bank fields
        if not all([bank_name, fullname, swift_code, currency, account_number]):
            return JsonResponse({
                "success": False,
                "message": "All bank details are required."
            })

        # Deduct from USDT balance
        balance.usdt_balance -= withdraw_amount
        balance.save()

        # Create bank withdrawal record (now includes amount)
        BankWithdrawal.objects.create(
            user=user,
            bank_name=bank_name,
            fullname=fullname,
            amount=withdraw_amount,
            account_number=account_number,
            swift_code=swift_code,
            currency=currency,
            status="Pending"
        )
        
        WithdrawTransaction.objects.create(
            user=user,
            currency=currency,
            withdraw_address="Bank Transfer",
            amount=withdraw_amount,
            tx_ref=str(uuid4()),
            status="pending",
        )

    else:
        return JsonResponse({"success": False, "message": "Invalid withdrawal type."})

    return JsonResponse({
        "success": True,
        "message": "Withdrawal request submitted successfully."
    })



def async_send_mail(*args, **kwargs):
    """Run send_mail in a background thread so it won't block the request."""
    threading.Thread(target=send_mail, args=args, kwargs=kwargs, daemon=True).start()


@login_required
def send_withdrawal_code(request):
    user = request.user

    try:
        transaction_code, created = TransactionCodes.objects.get_or_create(user=user)

        if created or not transaction_code.withdraw_code:
            withdrawal_code = str(random.randint(100000, 999999))
            transaction_code.withdraw_code = withdrawal_code
            transaction_code.withdraw_code_status = "active"
            transaction_code.save()
        else:
            withdrawal_code = transaction_code.withdraw_code

        # Email the code
        subject = "Your Withdrawal Code – Tesla Legacy Capital Partners"
        plain = (
            f"Dear {user.username},\n\n"
            f"Here is your personal withdrawal code: {withdrawal_code}\n\n"
            "This code is required for all withdrawals.\n\n"
            "Best Regards,\nTesla Legacy Capital Partners Support"
        )
        html = f"""
        <html><body>
          <h2 style="color:#0072ff;">Tesla Legacy Capital Partners</h2>
          <p>Dear {user.username},</p>
          <p>Your personal withdrawal code is:</p>
          <p style="font-size:20px;font-weight:bold;background:#f0f8ff;
                    padding:10px;display:inline-block;">
            {withdrawal_code}
          </p>
          <p>Please keep it safe and do not share it.</p>
        </body></html>
        """

        # Send asynchronously
        async_send_mail(
            subject,
            plain,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html,
            fail_silently=False,
        )

        return JsonResponse({
            "success": True,
            "message": "Your withdrawal code is being sent to your email."
        })

    except Exception as e:
        logger.exception("Error in send_withdrawal_code")
        return JsonResponse({
            "success": False,
            "message": f"Server error: {str(e)}"
        }, status=500)


@login_required
def verify_withdrawal_code(request):
    try:
        data = json.loads(request.body)
        entered_code = data.get("code", "").strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse(
            {"valid": False, "message": "Invalid request format."},
            status=400
        )

    user = request.user
    transaction_code = (
        TransactionCodes.objects
        .filter(user=user, withdraw_code_status="active")
        .first()
    )

    if transaction_code and entered_code == transaction_code.withdraw_code:
        return JsonResponse({
            "valid": True,
            "message": "Code verified. You may proceed with withdrawal."
        })

    return JsonResponse({
        "valid": False,
        "message": "Invalid or expired code."
    }, status=400)


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)

