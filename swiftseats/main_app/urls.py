from django.urls import path
from . import views
from .views import UserConcertListView, wishlist

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('concerts/', views.concert_index, name='index'),
    path('concerts/<int:concert_id>/', views.concert_detail, name='concert_detail'),
    path('accounts/signup/', views.signup, name='signup'),
    path('user-concerts/', UserConcertListView.as_view(), name='user-concerts'),
    path('wishlist/', wishlist, name='wishlist'),
    path('tickets/<int:ticket_id>/add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    path('wishlist/remove/<int:ticket_id>/', views.remove_from_wishlist, name='wishlist-remove'),
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),

]
