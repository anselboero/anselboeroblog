from django.contrib import admin

from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created', 'updated')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body')
    date_hierarchy = 'created'
