from django.conf.urls import url

from . import views

app_name = 'library'
urlpatterns = [
    # ex: /library/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /library/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /library/category/5
    url(r'^category/(?P<bundle_type_id>[0-9]+)/$', views.bundle_type_list, name='results'),
    # ex: /library/5/rate
    url(r'^(?P<bundle_id>[0-9]+)/rate/$', views.rate, name='rate'),
]