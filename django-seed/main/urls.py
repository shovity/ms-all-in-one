from django.contrib import admin
from django.urls import path

from core.api import Router

api = Router('django-seed/api')

api.add('temp/resource')

urlpatterns = []
urlpatterns.append(api.url())
