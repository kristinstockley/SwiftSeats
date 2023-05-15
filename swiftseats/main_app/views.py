from django.shortcuts import render
from .models import Concert

# Create your views here.
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