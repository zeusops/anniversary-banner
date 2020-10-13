from django.urls import path

from . import views

urlpatterns = [
    path('banner.png', views.banner, name='banner'),
    path('', views.index, name='index'),
]
