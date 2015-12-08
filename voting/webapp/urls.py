from django.conf.urls import url
from . import views
__author__ = 'Ezequiel Medina'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^evidences/(?P<id>[0-9]+)/$', views.get_evidence, name='get_evidence'),
]
