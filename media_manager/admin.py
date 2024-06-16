from django.contrib import admin
from .models import Event, FeaturedDesign, ArtProject, Tag, HennaDesign
from django_ckeditor_5.widgets import CKEditor5Widget


admin.site.register(FeaturedDesign)
admin.site.register(Event)


@admin.register(ArtProject)
class ArtProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'role', 'start_date', 'end_date', 'created_at')
    search_fields = ('title', 'role', 'description')
    list_filter = ('tags',)
    widgets = {
        "description": CKEditor5Widget(
            attrs={"class": "django_ckeditor_5"}, config_name='default'
        )
    }


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')


@admin.register(HennaDesign)
class HennaDesignAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_video')
    widgets = {
        "description": CKEditor5Widget(
            attrs={"class": "django_ckeditor_5"}, config_name='default'
        )
    }
