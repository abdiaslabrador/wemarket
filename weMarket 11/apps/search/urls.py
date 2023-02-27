
from django.conf.urls import url, include
from apps.search.views import index_by_category, index, searchProduct
from django.shortcuts import render, get_object_or_404

app_name = 'search'

urlpatterns = [
	url(r'^$', index, name="index"),
	url(r'^ajaxSearch', searchProduct, name="searchProduct"),#por nombre
	url(r'by(?P<id_category>\d+)/$', index_by_category, name="index_by_category"),#por categoria
]