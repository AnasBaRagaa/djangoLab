from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
# django.contrib.auth.models.User.objects.get(pk=2)

from django_countries.fields import CountryField

"""
owner : Anas Ba Ragaa

This based lab 11 and 12 requirements for CMP416


username = user
password = x
"""
# Create your models here.
class Contact(models.Model):
    person_name = models.CharField(max_length=200)
    person_address = models.CharField(max_length=300)
    person_age = models.IntegerField()
    added_on = models.DateTimeField('Added On')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return str(self.person_name)


class Entry(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    entry_value = models.CharField(max_length=100)
    entry_type = models.CharField(max_length=50)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)


    def __str__(self):
        return str(self.entry_value) + ':' + str(self.entry_type) + ' user=' + str(self.owner)


