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


class FeaturedDesign(models.Model):
    gif = models.ImageField(upload_to='images/')
    static_image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return os.path.basename(self.gif.name)


@receiver(post_save, sender=FeaturedDesign)
def create_static_image(sender, instance, created, **kwargs):
    if created and instance.gif.name.endswith('.gif'):
        gif_path = instance.gif.path
        static_image_path = gif_path.replace('.gif', '.jpg')
        print(f"Processing GIF: {gif_path}")

        try:
            with Image.open(gif_path) as img:
                num_frames = img.n_frames
                middle_frame_index = num_frames // 2
                img.seek(middle_frame_index)
                middle_frame = img.copy()
                middle_frame.save(static_image_path, format='JPEG')
                print(f"Saved static image to: {static_image_path}")

            instance.static_image = static_image_path.replace(settings.MEDIA_ROOT, '')
            instance.save()
            print(f"Updated static_image field for: {instance}")
        except Exception as e:
            print(f"Error processing GIF: {e}")


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
