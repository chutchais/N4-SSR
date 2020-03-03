from rest_framework import serializers
from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)

from rental.models import Rental

class RentalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Rental
		fields = ['container','che','terminal','rent_date','url']
		# lookup_field = 'slug'
		# extra_kwargs = {
		# 	'url': {'lookup_field': 'slug'}
		# }