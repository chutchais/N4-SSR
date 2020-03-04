from rest_framework import viewsets,filters
from rest_framework import status, viewsets
from rest_framework.decorators import action,detail_route
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response

from rental.models import Rental
from rental.api.serializers import RentalSerializer


class CreateListModelMixin(object):
	def create(self, request, *args, **kwargs):
		"""
			Create a list of model instances if a list is provides or a
			single model instance otherwise.
		"""
		data = request.data
		if isinstance(data, list):
			serializer = self.get_serializer(data=request.data, many=True)
		else:
			serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED,
					headers=headers)

class RentalViewSet(CreateListModelMixin,viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = Rental.objects.all()
	serializer_class = RentalSerializer
	filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
	search_fields = ()
	filter_fields = ()

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
	# lookup_field = 'slug'

