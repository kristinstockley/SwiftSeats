from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('concerts/', views.concert_index, name='index'),
  path('concerts/<int:concert_id>/', views.concert_detail, name='concert_detail'),
]