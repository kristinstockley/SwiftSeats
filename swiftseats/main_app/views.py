import os
import uuid
import boto3
from django.shortcuts import render, redirect, get_object_or_404
from .models import Concert, Ticket, Wishlist, Photo
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from datetime import date
from .forms import CreateConcertForm, EditConcertForm
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def concert_index(request):
    concerts = Concert.objects.all().exclude(attendees=request.user)
    return render(request, 'concerts/index.html', {'concerts': concerts})


class ConcertDetailView(LoginRequiredMixin, DetailView):
    model = Concert
    template_name = 'concerts/detail.html'
    context_object_name = 'concert'


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

class ConcertCreateView(LoginRequiredMixin, CreateView):
    model = Concert
    form_class = CreateConcertForm
    template_name = 'main_app/create_concert.html'

    def form_valid(self, form):
        concert = form.save(commit=False)
        concert.save()
        concert.attendees.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user-concerts', args=[self.request.user.id])



class ConcertDeleteView(LoginRequiredMixin, DeleteView):
    model = Concert
    template_name = 'concerts/delete.html'
    
    def get_success_url(self):
        return reverse_lazy('user-concerts', kwargs={'user_id': self.request.user.id})


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


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 10

    def get_queryset(self):
        concert_id = self.request.GET.get('concert_id')
        return Ticket.objects.filter(concert_id=concert_id)



class EditConcertView(LoginRequiredMixin, UpdateView):
    model = Concert
    form_class = EditConcertForm
    template_name = 'main_app/edit_concert.html'
    success_url = reverse_lazy('user-concerts')


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

    return redirect('user-concerts', user_id=request.user.id)


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'main_app/photo_delete.html'
    success_url = reverse_lazy('user-concerts')

    def get_success_url(self):
        return reverse_lazy('user-concerts', kwargs={'user_id': self.request.user.id})
    
@login_required
def add_to_attended(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    concert.attendees.add(request.user)
    return redirect('user-concerts', user_id=request.user.id)
