from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve 
from django.conf.urls import handler404, handler500


urlpatterns = [ 
    path('',views.first_view,name="first"),
    path('home/',views.home_view,name="home"),
    path('faQ/',views.faQ_view,name="faQ"),
    path('contact/',views.contact_view,name="contact"),
    path('academic/',views.academic_view,name="academic"),
    path('about/',views.about_view,name="about"),
    path('awards/',views.awards_view,name="awards"),
    path('affilate/',views.affilate_view,name="affilate"),
    path('news/',views.news_view,name="news"),
    path('tesla_cars/',views.tesla_cars_view,name="tesla_cars"),
    path('dash/',views.dash,name='dash'),
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name='login'),
    path('profile/',views.profile_view,name='profile'),
    path('referals/',views.referals,name='referals'),
    path('Deposit/',views.Deposit_view,name='Deposit'),
    path('purchase_plan/',views.purchase_plan,name='purchase_plan'),
    path('view_plans/',views.view_plans,name='view_plans'),
    path('withdraw/',views.withdraw_view,name='withdraw'),
    path('history/',views.history,name='history'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



handler404 = views.custom_404_view
handler500 = views.custom_500_view 

