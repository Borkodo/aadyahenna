# Generated by Django 4.2.13 on 2024-06-16 01:20

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media_manager', '0012_rename_video_hennadesign_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
    ]
