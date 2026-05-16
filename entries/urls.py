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
    path('<int:year>/<mm:month>/<mm:day>/<slug:slug>/', views.entry_detail, name='entry_detail'),
]
