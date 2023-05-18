from django.urls import path
from . import views
from .views import UserConcertListView, wishlist, create_concert

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
    path('concerts/create/', create_concert, name='create-concert'),
    path('concerts/<int:concert_id>/delete/', views.delete_concert, name='concert-delete'),
    path('concerts/<int:concert_id>/edit/', views.edit_concert, name='edit-concert'),
    path('concerts/<int:concert_id>/add_photo/', views.add_photo, name='add_photo'),


]
