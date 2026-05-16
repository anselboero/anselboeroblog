from django.shortcuts import get_object_or_404, render

from .models import Entry


def entry_list(request):
    entries = Entry.objects.all()
    return render(request, 'entries/entry_list.html', {'entries': entries})


def entry_detail(request, year, month, day, slug):
    entry = get_object_or_404(
        Entry,
        slug=slug,
        created__year=year,
        created__month=month,
        created__day=day,
    )
    return render(request, 'entries/entry_detail.html', {'entry': entry})
