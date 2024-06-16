from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from PIL import Image
import os
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field

class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#808080')

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Text', config_name='default')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.date >= timezone.now().date()


class ArtProject(models.Model):
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Text', config_name='default')
    image = models.ImageField(upload_to='art_projects/')
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


class HennaDesign(models.Model):
    file = models.FileField(upload_to='henna_designs/', blank=True)
    is_video = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"Henna Design {self.id}"
