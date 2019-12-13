from django.db import models
from django.urls import reverse

class Profile(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=254)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)


class Device(models.Model):
    user_id = models.BigIntegerField(db_index=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('seeker-home')

