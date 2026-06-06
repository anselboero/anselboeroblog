from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Entry, Person, Quote
from .quotes import extract_quotes


@receiver(post_save, sender=Entry)
def sync_entry_quotes(sender, instance, **kwargs):
    """Rebuild this entry's Quote rows from its body on every save.

    The body is the source of truth, so we replace the entry's quotes wholesale.
    Attributions pointing at a person slug that doesn't exist are skipped.
    Resolved people are also added to the entry's ``people`` M2M.
    """
    parsed = extract_quotes(instance.body)

    slugs = {q['slug'] for q in parsed}
    people = {p.slug: p for p in Person.objects.filter(slug__in=slugs)}

    instance.quotes.all().delete()
    Quote.objects.bulk_create([
        Quote(
            entry=instance,
            person=people[q['slug']],
            text=q['text'],
            source_url=q['source_url'],
            order=q['order'],
        )
        for q in parsed
        if q['slug'] in people
    ])

    matched = [people[s] for s in slugs if s in people]
    if matched:
        instance.people.add(*matched)
