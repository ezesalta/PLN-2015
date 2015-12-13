from django.conf.urls import url
from . import views
__author__ = 'Ezequiel Medina'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^evidences/(?P<id>[0-9]+)/$', views.get_evidence, name='get_evidence'),
    url(r'^load_laws/$', views.load_laws, name='load_laws'),
    url(r'^question/$', views.question, name='question'),
    url(r'^choice/$', views.save_choice, name='choice'),
    url(r'^results/$', views.results, name='results'),
]
