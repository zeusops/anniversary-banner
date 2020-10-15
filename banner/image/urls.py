from django.urls import path

from . import views

urlpatterns = [
    path('banner.jpg', views.banner),
    path('banner.png', views.banner),
    path('', views.index, name='index'),
]
