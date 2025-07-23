from django.db import models
from django.core.mail import send_mail
from django.conf import settings
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        pass

    def __str__(self):
        return f"{self.name} on {self.date} at {self.time}"


class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField(Event, related_name='participants')

    class Meta:
        pass

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            send_mail(
                'Welcome to the Event!',
                f'Hello {self.name},\n\nYou have been registered for the event(s).',
                settings.DEFAULT_FROM_EMAIL,
                [self.email],
                fail_silently=True,
            )