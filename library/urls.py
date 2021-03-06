from django.conf.urls import url

from . import views

app_name = 'library'
urlpatterns = [
    # ex: /library/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /library/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /library/category/toolkit/
    url(r'^category/(?P<bundle_type>[A-Za-z0-9_]+)/$', views.CategoryListView.as_view(), name='category'),
]