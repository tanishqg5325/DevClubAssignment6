from django.urls import path, include
from notes.views import index_view, add_note

app_name = 'notes'

urlpatterns = [
    path('', index_view, name='index'),
    path('addnote/', add_note, name='addnote'),
]
