from django.contrib import admin

from .models import Book, Entry, Movie, Person, Quote


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'book', 'movie', 'created', 'updated', 'is_published')
    list_filter = ('is_published', 'book', 'movie')
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


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'year', 'slug', 'created')
    list_filter = ('director',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'director__name')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """Read-only view; quotes are synced from entry bodies, not edited here."""
    list_display = ('person', 'short_text', 'entry', 'source_url')
    list_filter = ('person',)
    search_fields = ('text', 'person__name')

    @admin.display(description='quote')
    def short_text(self, obj):
        return obj.text[:80]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
