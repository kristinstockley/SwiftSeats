from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('concerts/', views.concert_index, name='index'),
    path('concerts/<int:pk>/', views.ConcertDetailView.as_view(), name='concert_detail'),
    path('user-concerts/<int:user_id>/', views.UserConcertListView.as_view(), name='user-concerts'),
    path('concerts/create/', views.ConcertCreateView.as_view(), name='create-concert'),
    path('concerts/<int:pk>/delete/', views.ConcertDeleteView.as_view(), name='concert-delete'),
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('tickets/<int:ticket_id>/add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    path('wishlist/remove/<int:ticket_id>/', views.remove_from_wishlist, name='wishlist-remove'),
    path('edit-concert/<int:pk>/', views.EditConcertView.as_view(), name='edit-concert'),
    path('concerts/<int:concert_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),
    path('concerts/<int:concert_id>/add-to-attended/', views.add_to_attended, name='add-to-attended'),
    path('delete-photo/<int:pk>/', views.PhotoDeleteView.as_view(), name='delete-photo'),
]
