from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('artist', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('venue', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=250)),
                ('attendees', models.ManyToManyField(blank=True, related_name='attended_concerts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('seat_number', models.CharField(max_length=10)),
                ('purchase_date', models.DateTimeField()),
                ('concerts', models.ManyToManyField(related_name='tickets', to='main_app.concert')),
            ],
        ),
    ]
