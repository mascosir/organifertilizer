

from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
   
    path("register/",views.signup),
    path("login/",views.login),
    path("blogs/",views.blogs),
    path("addBlogs/",views.AddBlogs),
    path("logout/",views.logout),
    path("News/",views.News),
    path("experts/",views.Experts),
    path("fertilizers/",views.Fertilizer),
    path("addFertilizers/",views.AddFertilizer),


    path("",views.index),
]   
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)