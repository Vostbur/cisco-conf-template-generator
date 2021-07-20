from django.urls import path

from .views import sshView


urlpatterns = [
    path('', sshView, name='ssh'),
]