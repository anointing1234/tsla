from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve 


urlpatterns = [ 
    path('',views.home_view,name="home"),
    path('faQ/',views.faQ_view,name="faQ"),
    path('contact/',views.contact_view,name="contact"),
    path('academic/',views.academic_view,name="academic"),
    path('about/',views.about_view,name="about"),
    path('awards/',views.awards_view,name="awards"),
    path('affilate/',views.affilate_view,name="affilate"),
    path('news/',views.news_view,name="news"),
    path('tesla_cars/',views.tesla_cars_view,name="tesla_cars"),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



 

