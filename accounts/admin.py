from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Account, Balance ,ForexPlan,DepositTransaction,WithdrawTransaction,WalletAddress, Referral, PaymentGateway,Users_Investment,TransactionCodes,BankWithdrawal
from django.utils.html import format_html
from django.conf import settings
from django.urls import reverse
from django.urls import path
from django.http import JsonResponse
from django.db.models import F
import uuid
from decimal import Decimal


class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Confirm Password"), widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'fullname', 'phone', 'country')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords do not match"))
        return password2

    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(self.cleaned_data["password1"])
        if commit:
            account.save()
        return account

@admin.register(Account)
class AccountAdmin(BaseUserAdmin, UnfoldModelAdmin):
    ordering = ('-date_joined',)
    list_display = ('display_profile_picture','email', 'fullname', 'phone', 'country', 'is_staff', 'is_active','raw_password',)
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    readonly_fields = ('date_joined', 'last_login', 'profile_picture_preview','raw_password')  # Add profile picture preview

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('fullname', 'phone', 'country', 'profile_picture', 'profile_picture_preview')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'phone', 'country', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'fullname', 'phone')
    filter_horizontal = ('groups', 'user_permissions',)
    
    add_form = AccountCreationForm

    # Display profile picture in the admin list
    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%;" />', obj.profile_picture.url)
        return "No Image"

    display_profile_picture.short_description = "Profile Picture"

    # Show a large preview of the profile picture in the detail view
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="width: 150px; height: 150px; object-fit: cover; border-radius: 10px;" />', obj.profile_picture.url)
        return "No Image"

    profile_picture_preview.short_description = "Profile Picture Preview"

    # Show total users in the admin changelist
    def changelist_view(self, request, extra_context=None):
        User = get_user_model()
        total_users = User.objects.count()
        messages.info(request, f'Total Users: {total_users}')
        return super().changelist_view(request, extra_context=extra_context)



@admin.register(Balance)
class BalanceAdmin(UnfoldModelAdmin):
    list_display = ('user', 'usdt_balance', 'total_profits', 'invested_amount')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('user',)

    def save_model(self, request, obj, form, change):
        """
        Whenever the admin edits a Balance, if usdt_balance or invested_amount
        increases, create a corresponding DepositTransaction.
        """
        if change:
            # Fetch the old values from the database
            old = Balance.objects.get(pk=obj.pk)
            
            # Compute deltas
            delta_balance = obj.usdt_balance - old.usdt_balance
            delta_invested = obj.invested_amount - old.invested_amount

            # If the admin has increased the USDT balance:
            if delta_balance > Decimal('0.00'):
                DepositTransaction.objects.create(
                    user=obj.user,
                    method='Deposit',
                    amount=delta_balance,
                    tx_ref=str(uuid.uuid4()),
                    status='completed'
                )

            # If the admin has increased the invested amount:
            if delta_invested > Decimal('0.00'):
                DepositTransaction.objects.create(
                    user=obj.user,
                    method='Invested',
                    amount=delta_invested,
                    tx_ref=str(uuid.uuid4()),
                    status='completed'
                )

        # Finally, save the (possibly updated) Balance object
        super().save_model(request, obj, form, change)



@admin.register(ForexPlan)
class ForexPlanAdmin(UnfoldModelAdmin):
    list_display = ('name', 'percentage', 'duration', 'min_amount', 'max_amount', 'commission', 'capital_insurance')
    search_fields = ('name', 'duration')
    list_filter = ('percentage', 'duration', 'commission', 'capital_insurance')





User = settings.AUTH_USER_MODEL  # Custom User Model


@admin.register(WalletAddress)
class WalletAddressAdmin(UnfoldModelAdmin):
    list_display = ("user", "currency", "address")
    search_fields = ("user__email", "currency")
    list_filter = ("currency",)


@admin.register(Referral)
class ReferralAdmin(UnfoldModelAdmin):
    list_display = ("user", "email", "referral_code")
    search_fields = ("email", "referral_code")


@admin.register(PaymentGateway)
class PaymentGatewayAdmin(UnfoldModelAdmin):
    list_display = ("wallet_address", "currency")
    search_fields = ("wallet_address", "currency")


@admin.register(DepositTransaction)
class DepositTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "method", "tx_ref", "date", "status", "screenshot_preview", "confirm_button", "decline_button")
    search_fields = ("user__email", "tx_ref")
    list_filter = ("status", "method", "date")

    def screenshot_preview(self, obj):
        if obj.screenshot:
            return format_html('<img src="{}" style="width: 100px; height: auto; border-radius: 5px;" />', obj.screenshot.url)
        return "No Image"

    screenshot_preview.short_description = "Screenshot"

    def confirm_button(self, obj):
        if obj.status == "pending":
            confirm_url = reverse("confirm_deposit", args=[obj.pk])  # Use reverse to generate correct URL
            return format_html('<a class="button" href="{}" style="background: green; color: white; padding: 5px 10px; border-radius: 5px;">Confirm</a>', confirm_url)
        return "✅ Completed"

    def decline_button(self, obj):
        if obj.status == "pending":
            decline_url = reverse("decline_deposit", args=[obj.pk])  # Use reverse to generate correct URL
            return format_html('<a class="button" href="{}" style="background: red; color: white; padding: 5px 10px; border-radius: 5px;">Decline</a>', decline_url)
        return "❌ Failed"

    confirm_button.short_description = "Confirm"
    decline_button.short_description = "Decline"



@admin.register(WithdrawTransaction)
class WithdrawTransactionAdmin(UnfoldModelAdmin):
    list_display = (
        "user", "withdraw_address", "currency", "amount", "tx_ref", 
        "date", "status", "confirm_button", "decline_button"
    )
    search_fields = ("user__email", "tx_ref")
    list_filter = ("status", "currency", "date")

    def confirm_button(self, obj):
        if obj.status == "pending":
            url = reverse("confirm_withdraw", args=[obj.pk])
            return format_html('<a class="button btn btn-success" href="{}">Confirm</a>', url)
        return "Completed"

    def decline_button(self, obj):
        if obj.status == "pending":
            url = reverse("decline_withdraw", args=[obj.pk])
            return format_html('<a class="button btn btn-danger" href="{}">Decline</a>', url)
        return "Failed"

    confirm_button.short_description = "Confirm"
    decline_button.short_description = "Decline"


@admin.register(Users_Investment)
class UsersInvestmentAdmin(UnfoldModelAdmin):
    list_display = ('user', 'uniq_id', 'plan', 'profit', 'total', 'start_date', 'end_date', 'status', 'ends_in', 'elapsed')
    search_fields = ('user__email', 'uniq_id', 'plan__name')
    list_filter = ('status', 'start_date', 'end_date')

    def ends_in(self, obj):
        return obj.ends_in()
    
    def elapsed(self, obj):
        return obj.elapsed()

    ends_in.short_description = "Ends In (Days)"
    elapsed.short_description = "Elapsed (Days)"







@admin.register(TransactionCodes)
class TransactionCodesAdmin(UnfoldModelAdmin):
    list_display = ("user", "withdraw_code", "withdraw_code_status", "reset_code", "reset_code_status", "withdraw_code_created_at", "reset_code_created_at")
    list_filter = ("withdraw_code_status", "reset_code_status")
    search_fields = ("user__username", "withdraw_code", "reset_code")
    readonly_fields = ("withdraw_code_created_at", "reset_code_created_at")

    def has_add_permission(self, request):
        """Disable manual addition from admin (codes should be generated automatically)."""
        return False

admin.site.site_header = "Transaction Codes Management"
admin.site.site_title = "Transaction Codes Admin"
admin.site.index_title = "Manage Transaction Codes"




@admin.action(description="Mark selected withdrawals as Confirmed (Successful)")
def mark_as_confirmed(modeladmin, request, queryset):
    queryset.update(status="Successful")

@admin.action(description="Mark selected withdrawals as Declined (Rejected)")
def mark_as_declined(modeladmin, request, queryset):
    queryset.update(status="Rejected")


@admin.register(BankWithdrawal)
class BankWithdrawalAdmin(UnfoldModelAdmin):
    list_display = ("user", "bank_name", "fullname", "account_number", "currency", "status", "created_at")
    list_filter = ("status", "currency", "created_at")
    search_fields = ("user__email", "bank_name", "account_number", "fullname")
    actions = [mark_as_confirmed, mark_as_declined]
    readonly_fields = ("user", "bank_name", "fullname", "account_number", "swift_code", "currency", "created_at")

    def has_change_permission(self, request, obj=None):
        if obj and obj.status in ["Successful", "Rejected"]:
            return False
        return super().has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Update the corresponding WithdrawTransaction with withdraw_address='Bank Transfer'
        WithdrawTransaction.objects.filter(
            user=obj.user,
            amount=obj.amount,
            currency=obj.currency,
            withdraw_address="Bank Transfer",
            status="pending"
        ).update(status=self._map_bank_status(obj.status))

    def _map_bank_status(self, bank_status):
        # Maps bank withdrawal status to WithdrawTransaction status
        mapping = {
            "Pending": "pending",
            "Successful": "completed",
            "Rejected": "failed"
        }
        return mapping.get(bank_status, "pending")  # fallback to pending
