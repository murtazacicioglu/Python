
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('kayit/', views.kayit, name="kayit"),
    path('sifreunuttum/', views.sifreunuttum, name="sifreunuttum"),
    path('giris1/', views.giris1, name="giris1"),

]