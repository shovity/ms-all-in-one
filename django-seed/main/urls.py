from django.contrib import admin
from django.urls import path

from core.api import APIBase

class T(APIBase):

    def get(self):
        return self.res(1)

urlpatterns = [
    path('django-seed/', T.as_view())
]
