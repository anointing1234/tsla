from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve 
from django.conf.urls import handler404, handler500


urlpatterns = [ 
    path('register/',views.register,name='register'),
    path('login_view/',views.login_view,name='login_view'),
    path('logout_view/',views.logout_view,name='logout_view'),
    path('send_pass/',views.send_pass_views,name='send_pass'),
    path('reset_pass/',views.reset_pass,name='reset_pass'),
    path('send_reset_code/',views.send_reset_code,name='send_reset_code'),
    path("verify_reset_code/",views.verify_reset_code, name="verify_reset_code"),
    path("confirm-deposit/<int:pk>/",views.confirm_deposit_view, name="confirm_deposit"),
    path("decline-deposit/<int:pk>/",views.decline_deposit_view, name="decline_deposit"),
    path('withdraw_funds/',views.withdraw_funds,name='withdraw_funds'),
    path('send_withdrawal_code/',views.send_withdrawal_code,name='send_withdrawal_code'),
    path('verify_withdrawal_code/',views.verify_withdrawal_code,name='verify_withdrawal_code'),
    path('confirm-withdraw/<int:withdraw_id>/',views.confirm_withdraw, name='confirm_withdraw'),
    path('decline-withdraw/<int:withdraw_id>/',views.decline_withdraw, name='decline_withdraw'),
    path("update-profile-picture/",views.update_profile_picture, name="update_profile_picture"),
    path("update_profile/",views.update_profile, name="update_profile"),
    path("update_password/",views.update_password, name="update_password"),
    path("update_withdrawal/",views.update_withdrawal_account, name="update_withdrawal"),
    path("deposit/",views.deposit_funds, name="deposit"),
    path("quick-trade/", views.quick_trade, name="quick_trade"),
    path('purchase-plan/',views.purchase_plan_view,name='purchase-plan'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = views.custom_404_view
handler500 = views.custom_500_view



 

