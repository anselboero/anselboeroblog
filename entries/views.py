from django.shortcuts import get_object_or_404, render

from .models import Entry


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
