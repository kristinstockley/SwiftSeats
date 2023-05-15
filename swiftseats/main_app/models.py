from django.db import models


# Create your models here.
class Concert(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    
    def __str__(self):
        return self.title
