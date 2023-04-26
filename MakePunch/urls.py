from django.contrib import admin
from django.urls import path, include
from .views import makePunch

urlpatterns = [
    path('', makePunch),
]
