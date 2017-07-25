from django.conf.urls import url

from . import views

app_name = 'nodectl'
urlpatterns = [
    # ex: /nodectl/
    url(r'^$', views.index, name='index'),
    # ex /nodectl/node/2/
    url(r'^node/(?P<node_id>[0-9]+)$', views.node, name='node'),
]