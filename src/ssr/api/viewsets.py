from rest_framework import viewsets,filters
from rest_framework import status, viewsets
from rest_framework.decorators import action,detail_route
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ssr.models import Ssr,Ssrfiles
from ssr.api.serializers import SsrSerializer


class SsrViewSet(viewsets.ModelViewSet):
	queryset = Ssr.objects.all()
	serializer_class = SsrSerializer
	filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
	search_fields = ()
	filter_fields = ()
	lookup_field = 'number'

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
	# lookup_field = 'slug'

class SsrFilesViewSet(viewsets.ModelViewSet):
	queryset = Ssrfiles.objects.all()
	serializer_class = SsrSerializer
	filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
	search_fields = ()
	filter_fields = ()
	lookup_field = 'ssr'