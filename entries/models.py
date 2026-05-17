from django.db import models
from django.urls import reverse
from django.utils import timezone


class Person(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    bio = models.TextField(blank=True)
    url = models.URLField(blank=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('person_detail', kwargs={'slug': self.slug})


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name='books',
    )
    slug = models.SlugField(max_length=200, unique=True)
    cover_url = models.URLField(blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    goodreads_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title} — {self.author}'

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})


class Entry(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entries',
    )
    people = models.ManyToManyField(
        Person,
        blank=True,
        related_name='entries',
    )

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
