
from django.db import models
from django.conf import settings
from django.utils.timezone import now


# Create your models here.


class Abonent(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='abonents')


class Phone(models.Model):
    abonent = models.ForeignKey(
        Abonent, on_delete=models.CASCADE, related_name='phones')
    phone = models.CharField(max_length=30)


class Email(models.Model):
    abonent = models.ForeignKey(
        Abonent, on_delete=models.CASCADE, related_name='emails')
    email = models.EmailField()


class Note(models.Model):
    abonent = models.ForeignKey(
        Abonent, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    date = models.DateField(default=now)


class Tag(models.Model):
    note = models.ManyToManyField(Note, related_name='tags')
    tag = models.CharField(max_length=20, unique=True)
