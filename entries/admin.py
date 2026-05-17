from django.contrib import admin

from .models import Book, Entry, Person


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'book', 'created', 'updated', 'is_published')
    list_filter = ('is_published', 'book')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body')
    date_hierarchy = 'created'
    filter_horizontal = ('people',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'created')
    list_filter = ('author',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'author__name', 'isbn')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
