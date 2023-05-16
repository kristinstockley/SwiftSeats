from django.shortcuts import render, redirect
from .models import Concert, Ticket, Wishlist
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from faker import Faker


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def concert_index(request):
    concerts = Concert.objects.all()
    return render(request, 'concerts/index.html', {'concerts': concerts})

def concert_detail(request, concert_id):
    concert = Concert.objects.get(id=concert_id)
    return render(request, 'concerts/detail.html', {'concert': concert})



class UserConcertListView(LoginRequiredMixin, ListView):
    model = Concert
    template_name = 'main_app/user_concert_list.html'
    context_object_name = 'concerts'

    def get_queryset(self):
        user = self.request.user
        return Concert.objects.filter(attendees=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['attended_concerts'] = user.attended_concerts.all()
        return context


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def add_to_wishlist(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.tickets.add(ticket)
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.tickets.remove(ticket)
    return redirect('wishlist')

@login_required
def wishlist(request):
    try:
        wishlist = Wishlist.objects.get(user=request.user)
    except Wishlist.DoesNotExist:
        wishlist = None
    return render(request, 'main_app/wishlist.html', {'wishlist': wishlist})



class TicketListView(ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 10

    def get_queryset(self):
        concert_id = self.request.GET.get('concert_id')
        return Ticket.objects.filter(concert_id=concert_id)


    

class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['concert'] = self.object.concert
        return context

class TicketUpdateView(UpdateView):
    model = Ticket
    template_name = 'tickets/update.html'
    fields = ['price', 'seat_number', 'concert']
    context_object_name = 'ticket'



def generate_fake_tickets(request):
    fake = Faker()
    concerts = Concert.objects.all()
    tickets = []

    for concert in concerts:
        for _ in range(10):
            price = fake.random_int(min=10, max=100)
            seat_number = fake.random_int(min=100, max=999)
            ticket = Ticket(price=price, seat_number=seat_number, concert=concert)
            tickets.append(ticket)

    Ticket.objects.bulk_create(tickets)
    return redirect('ticket-list')
