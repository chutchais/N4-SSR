from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

# from .views import (OperationDetailView,
# 					OperationListView,
# 					onwip)

from .views import rental_report

urlpatterns = [
	# Page
	url(r'^$',rental_report,name='rental-report'),
	# url(r'^(?P<slug>[-\w]+)/$',OperationDetailView.as_view(),name='detail'),
 #    url(r'^(?P<slug>[-\w]+)/wip/$',onwip,name='wip'),

]