import os
import uuid
import boto3
from django.shortcuts import render, redirect, get_object_or_404
from .models import Concert, Ticket, Wishlist, Photo
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, UpdateView
from django.contrib.auth.decorators import login_required
from .forms import CreateConcertForm, EditConcertForm




def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def concert_index(request):
    concerts = Concert.objects.all()
    concerts = Concert.objects.exclude(attendees=request.user)
    return render(request, 'concerts/index.html', {'concerts': concerts})

def concert_detail(request, concert_id):
    concert = Concert.objects.get(id=concert_id)
    tickets = concert.tickets.all()

    return render(request, 'concerts/detail.html', {'concert': concert, 'tickets': tickets})


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


@login_required
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



class TicketUpdateView(UpdateView):
    model = Ticket
    template_name = 'tickets/update.html'
    fields = ['price', 'seat_number', 'concert']
    context_object_name = 'ticket'


@login_required
def create_concert(request):
    if request.method == 'POST':
        form = CreateConcertForm(request.POST)
        if form.is_valid():
            concert = form.save(commit=False)
            concert.save()
            concert.attendees.add(request.user)
            return redirect('user-concerts')
    else:
        form = CreateConcertForm()
    return render(request, 'main_app/create_concert.html', {'form': form})


@login_required
def delete_concert(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    if request.method == 'POST':
        concert.delete()
        return redirect('user-concerts')
    return redirect('concert-detail', concert_id=concert_id)


@login_required
def edit_concert(request, concert_id):
    concert = get_object_or_404(Concert, pk=concert_id)
    if request.method == 'POST':
        form = EditConcertForm(request.POST, instance=concert)
        if form.is_valid():
            form.save()
            return redirect('concert_detail', concert_id=concert_id)
    else:
        form = EditConcertForm(instance=concert)
        return render(request, 'main_app/edit_concert.html', {'form': form, 'concert': concert})
    



def add_photo(request, concert_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, concert_id=concert_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
            
        return redirect('user-concerts')
