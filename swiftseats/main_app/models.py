from django.db import models
from django.contrib.auth.models import User


class Concert(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    date = models.DateField()
    venue = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    attendees = models.ManyToManyField(User, related_name='attended_concerts', blank=True)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    seat_number = models.CharField(max_length=10)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='tickets')

    def __str__(self):
        return str(self.pk)


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)

    def __str__(self):
        return f"Wishlist for {self.user.username}"

class Photo(models.Model):
    url = models.CharField(max_length=200)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for concert_id: {self.concert_id} @{self.url}"
