# Generated by Django 4.2.13 on 2024-06-16 02:10

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('media_manager', '0014_alter_event_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artproject',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text'),
        ),
    ]