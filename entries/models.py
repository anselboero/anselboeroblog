from django.db import models
from django.urls import reverse
from django.utils import timezone


class Entry(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        created = timezone.localtime(self.created)
        return reverse('entry_detail', kwargs={
            'year': created.year,
            'month': created.month,
            'day': created.day,
            'slug': self.slug,
        })
