from django.urls import path, register_converter

from . import views


class TwoDigitConverter:
    regex = r'\d{2}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return f'{int(value):02d}'


register_converter(TwoDigitConverter, 'mm')

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('books/', views.book_list, name='book_list'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<slug:slug>/', views.movie_detail, name='movie_detail'),
    path('people/', views.person_list, name='person_list'),
    path('people/<slug:slug>/', views.person_detail, name='person_detail'),
    path('quotes/', views.quote_list, name='quote_list'),
    path('<int:year>/<mm:month>/<mm:day>/<slug:slug>/', views.entry_detail, name='entry_detail'),
]
