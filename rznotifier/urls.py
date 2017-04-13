from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^fetch-loans/$', views.fetch_loans, name='fetch_loans'),
]
