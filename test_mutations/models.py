from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    creation_date = models.DateTimeField(auto_now=True)

    # Double underscore methods
    def __str__(self):
        return self.username


class IsolatedModel(models.Model):
    integer_field = models.IntegerField()
    char_field = models.CharField(max_length=255)
    float_field = models.FloatField(null=True)
    text_field = models.TextField(null=True)
    decimal_field = models.DecimalField(decimal_places=2, max_digits=8)
    booleanField = models.BooleanField(null=True)
    date_field = models.DateField(null=True)
    date_time_field = models.DateTimeField(null=True)
    file_field = models.FileField(null=True)


class RelationshipReceiverModel(models.Model):
    name = models.CharField(max_length=255)


class RelationshipSenderModel(models.Model):
    name = models.CharField(max_length=255)
    foreign_key = models.ForeignKey(
        RelationshipReceiverModel,
        on_delete=models.CASCADE
    )
    many_to_many = models.ManyToManyField(
        RelationshipReceiverModel,
        related_name="sender_many_to_many"
    )
