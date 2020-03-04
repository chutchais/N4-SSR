from django.shortcuts import render
from django.db.models import Q
from django.db.models import (ExpressionWrapper,F,Min,Max,Avg,StdDev,Count,Sum,
							Value, When,Case,IntegerField,CharField,FloatField)
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django.db.models.functions import Floor,Ceil
from django.db.models.functions import Mod

# Create your views here.
from django.http import JsonResponse

from .models import Rental,Kind

def rental_report(request):
	
	terminal	 		= request.GET.get('terminal')
	str_start_date 		= request.GET.get('start_date')
	str_stop_date 		= request.GET.get('stop_date')
	detail 				= request.GET.get('detail')
	return JsonResponse(get_rental(terminal,str_start_date,str_stop_date,detail), safe=False)
	
def get_rental(terminal,str_start_date,str_stop_date,detail):
	rentel_list = get_rental_detail(terminal,str_start_date,str_stop_date)
	
	# if need details 
	if detail == 'yes':
		return  rentel_list

	# Default is summary by CHE Kind
	kinds = Kind.objects.all().order_by('name')
	kind_list = list(kinds.values('name','title'))
	for kind in kind_list:
		x,y = get_kind_total_hour(rentel_list,kind['name'])
		# print(kind['name'],x,y)
		kind['total_hours'] 		=	x
		kind['total_containers'] 	=	y
	return kind_list



def get_kind_total_hour(rental_list,kind):
	sum_total_hours = 0
	sum_total_container = 0

	for i in rental_list :
		if i['che__kind']== kind:
			sum_total_hours =+ i['total_hours']
			sum_total_container =+ i['total_containers']

	return sum_total_hours,sum_total_container



def get_rental_detail(terminal,str_start_date,str_stop_date):
	import math
	from datetime import datetime, timedelta
	start_date 			= None
	stop_date 			= None
	container_list 		= {}

	if terminal and str_start_date and str_stop_date :
		start_date = datetime.strptime(str_start_date, "%Y-%m-%d").date()
		stop_date = datetime.strptime(str_stop_date, "%Y-%m-%d").date() + timedelta(days=1)
		
		rentals = Rental.objects.filter(terminal=terminal,
									rent_date__range=[start_date,stop_date])
		reports 	= rentals.values('rent_date__date','che__kind').annotate(
								total_containers = Count('container'),
								total_handling_time = Sum('che__kind__handling_time'),
								transportation_time = Max('che__kind__trans_time'),
								total_minutes =F('total_handling_time')+F('transportation_time'),
								mod_minute = Floor(F('total_minutes')/60),
								total_hours = Floor(F('total_minutes')/60)).order_by('rent_date__date','che__kind')
		
		for r in reports:
			mod_minute = r['total_minutes'] % 60
			hours 	= math.floor(r['total_minutes'] / 60)
			hours 	= hours + (0.5 if mod_minute > 0 and mod_minute < 30 else 0)
			hours 	= hours + (1 if mod_minute >= 30 else 0)
			r['mod_minute'] = mod_minute
			r['total_hours'] = hours
			# print(r['total_minutes'], hours,mod_minute)

		container_list = list(reports)

	return container_list


	# reports 	= rentals.values('rent_date__date','che__kind').annotate(
	# 						total_containers = Count('container'),
	# 						total_handling_time = Sum('che__kind__handling_time'),
	# 						transportation_time = Max('che__kind__trans_time'),
	# 						total_time =F('total_handling_time')+F('transportation_time'),
	# 						mod_minute = Mod(F('total_time'),60),
	# 						total_hours = Floor(F('total_time')/60) + 
	# 							Case(When(mod_minute__gt =  30 , then=Value(1)),
	# 								When(mod_minute__range =  [1,29] , then=Value(0.5)),
	# 								default = Value(0),
	#         						output_field = FloatField())
	# 						).order_by('rent_date__date','che__kind')


		# reports 	= rentals.values('rent_date__date','che__kind').annotate(
		# 						total_containers = Count('container'),
		# 						total_handling_time = Sum('che__kind__handling_time'),
		# 						transportation_time = Max('che__kind__trans_time'),
		# 						total_time = ExpressionWrapper(F('total_handling_time')+F('transportation_time'),output_field=IntegerField()),
		# 						mod_minute = ExpressionWrapper(Mod(62,60),output_field=IntegerField()),
		# 						total_hours = F('total_handling_time')/60).order_by(
		# 						'rent_date__date','che__kind')