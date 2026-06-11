from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Book, Entry, Movie, Person, Quote


def _visible_entries(request):
    if request.user.is_authenticated and request.user.is_staff:
        return Entry.objects.all()
    return Entry.objects.filter(is_published=True)


def entry_list(request):
    entries = _visible_entries(request)
    return render(request, 'entries/entry_list.html', {'entries': entries})


def entry_detail(request, year, month, day, slug):
    entry = get_object_or_404(
        _visible_entries(request),
        slug=slug,
        created__year=year,
        created__month=month,
        created__day=day,
    )
    return render(request, 'entries/entry_detail.html', {'entry': entry})


def book_list(request):
    books = Book.objects.all()
    return render(request, 'entries/book_list.html', {'books': books})


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'entries/movie_list.html', {'movies': movies})


def person_list(request):
    people = Person.objects.all()
    return render(request, 'entries/person_list.html', {'people': people})


def quote_list(request):
    quotes = (
        Quote.objects.filter(entry__in=_visible_entries(request))
        .select_related('person', 'entry')
        .order_by('-entry__created', 'order')
    )
    return render(request, 'entries/quote_list.html', {'quotes': quotes})


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    entries = _visible_entries(request).filter(book=book)
    return render(request, 'entries/book_detail.html', {'book': book, 'entries': entries})


def movie_detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    entries = _visible_entries(request).filter(movie=movie)
    return render(request, 'entries/movie_detail.html', {'movie': movie, 'entries': entries})


def person_detail(request, slug):
    person = get_object_or_404(Person, slug=slug)
    entries = _visible_entries(request).filter(
        Q(people=person) | Q(book__author=person) | Q(movie__director=person)
    ).distinct()
    quotes = (
        person.quotes.filter(entry__in=_visible_entries(request))
        .select_related('entry')
        .order_by('-entry__created', 'order')
    )
    return render(request, 'entries/person_detail.html', {
        'person': person,
        'entries': entries,
        'books': person.books.all(),
        'movies': person.movies.all(),
        'quotes': quotes,
    })
