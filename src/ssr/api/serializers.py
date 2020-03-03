from rest_framework import serializers
from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)

from ssr.models import Ssr,Ssrfiles

class SsrFilesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ssrfiles
		fields = ['file','note']

class SsrSerializer(serializers.ModelSerializer):
	files = SsrFilesSerializer(many=True, read_only=True)
	class Meta:
		model = Ssr
		fields = ['number','title','completed','files','url']
		lookup_field = 'number'
		extra_kwargs = {
			'url': {'lookup_field': 'number'}
		}