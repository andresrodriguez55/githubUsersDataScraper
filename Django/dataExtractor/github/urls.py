from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('extractData', views.extractData),
    path('saveData', views.createGithubUser, name = 'saveData'),
    path('extractedData', views.extractedData),
]
