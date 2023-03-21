from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from smpptransfer.api.views import read_unread_messages, read_all_messages, send_messages

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('retrieve/unread', read_unread_messages, name='read_unread_messages'),
    path('retrieve/all', read_all_messages, name='read_all_messages'),
    path('send', send_messages, name='send_messages'),
]

# urlpatterns += router.urls
