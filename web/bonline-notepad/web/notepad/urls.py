from django.urls import path
from . import views

app_name = 'notepad'

urlpatterns = [
    path('', views.index, name='index'),
    path('note/<uuid:noteid>', views.note, name='note'),
    path('sendToGalih', views.sendToGalih, name='sendToGalih'),
    path('superSecretGalih6fa0798464cd8cb100628e56da3fdf41', views.superSecretGalih, name='superSecretGalih'),
]