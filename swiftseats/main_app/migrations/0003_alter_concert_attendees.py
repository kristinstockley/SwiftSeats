# Generated by Django 4.2.1 on 2023-05-17 20:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0002_remove_ticket_concerts_remove_ticket_purchase_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concert',
            name='attendees',
            field=models.ManyToManyField(related_name='attended_concerts', to=settings.AUTH_USER_MODEL),
        ),
    ]
