from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Book, Entry, Person


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


def person_list(request):
    people = Person.objects.all()
    return render(request, 'entries/person_list.html', {'people': people})


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    entries = _visible_entries(request).filter(book=book)
    return render(request, 'entries/book_detail.html', {'book': book, 'entries': entries})


def person_detail(request, slug):
    person = get_object_or_404(Person, slug=slug)
    entries = _visible_entries(request).filter(
        Q(people=person) | Q(book__author=person)
    ).distinct()
    return render(request, 'entries/person_detail.html', {
        'person': person,
        'entries': entries,
        'books': person.books.all(),
    })
