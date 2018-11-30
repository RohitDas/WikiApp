from django.urls import path, re_path

from . import views

app_name = 'querymanager'
urlpatterns = [
    path('', views.index, name='index'),
    path('send', views.query, name='query'),
    path('general_send', views.general_query, name='general_query'),
    re_path(r'^results[(?P<page>\d+)]*$', views.results, name='result'),
    path('general_results', views.general_results, name='general_results'),
    path('category_view', views.category_view, name='category_view'),
    path('get_most_outdated', views.get_most_outdated, name='get_most_outdated'),
    path('recent', views.recent, name='recent')
]