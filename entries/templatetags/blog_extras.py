import json
from urllib.error import URLError
from urllib.request import urlopen

import markdown as md
from django import template
from django.core.cache import cache
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='markdown')
def markdown_filter(value):
    html = md.markdown(
        value,
        extensions=['fenced_code', 'tables', 'smarty', 'toc'],
        extension_configs={'toc': {'anchorlink': True}},
    )
    return mark_safe(html)


LAST_MOVIE_URL = 'https://storage.googleapis.com/anselboero-website-prod-apis/last_movie_watched.json'
LAST_MOVIE_CACHE_KEY = 'last_movie_watched'
LAST_MOVIE_CACHE_TTL = 60 * 15


@register.simple_tag
def last_movie():
    cached = cache.get(LAST_MOVIE_CACHE_KEY)
    if cached is not None:
        return cached
    try:
        with urlopen(LAST_MOVIE_URL, timeout=2) as response:
            data = json.load(response)
    except (URLError, OSError, json.JSONDecodeError):
        return None
    movie = {
        'title': data.get('last_watched__title'),
        'rating': data.get('last_watched__rating'),
        'imdb_link': data.get('last_watched__imdb_link'),
        'poster_link': data.get('last_watched__poster_link'),
        'review_link': data.get('last_watched__review_link'),
    }
    cache.set(LAST_MOVIE_CACHE_KEY, movie, LAST_MOVIE_CACHE_TTL)
    return movie


CURRENTLY_READING_URL = 'https://storage.googleapis.com/anselboero-website-prod-apis/currently_reading_book.json'
CURRENTLY_READING_CACHE_KEY = 'currently_reading_book'
CURRENTLY_READING_CACHE_TTL = 60 * 15


@register.simple_tag
def currently_reading():
    cached = cache.get(CURRENTLY_READING_CACHE_KEY)
    if cached is not None:
        return cached
    try:
        with urlopen(CURRENTLY_READING_URL, timeout=2) as response:
            data = json.load(response)
    except (URLError, OSError, json.JSONDecodeError):
        return None
    book = {
        'title': data.get('currently_reading__title'),
        'goodreads_link': data.get('currently_reading__goodreads_link'),
        'poster_link': data.get('currently_reading__poster_link'),
        'quote': data.get('currently_reading__quote'),
        'personal_website_link': data.get('currently_reading__personal_website_link'),
    }
    cache.set(CURRENTLY_READING_CACHE_KEY, book, CURRENTLY_READING_CACHE_TTL)
    return book
