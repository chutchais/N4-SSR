from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from django.db.models import (ExpressionWrapper,F,Min,Max,Avg,StdDev,Count,Sum,
							Value, When,Case,IntegerField,CharField,FloatField)
from django.db.models.functions import Floor,Ceil
import math
import datetime
import calendar

from django.utils import timezone
# Register your models here.
from .models import Kind,Rental,Che

class RentalResource(resources.ModelResource):
	class Meta:
		model               = Rental
		import_id_fields    = ()
		skip_unchanged      = True
		report_skipped      = True
		fields              = ('container','terminal','che','rent_date')

class RentalAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields           = ['container','terminal','che__name']
	list_filter             = ['terminal']
	list_display            = ('container','terminal','che','rent_date','created','user')
	readonly_fields         = ('created','modified','user')

	# save_as = True
	# save_as_continue = True
	# save_on_top =True

	fieldsets = [
		('Basic Information',{'fields': ['container','terminal','che','rent_date']}),
		('System Information',{'fields':['user','created','modified']})
	]
	resource_class          = RentalResource

	def save_model(self, request, obj, form, change):
		obj.user = request.user
		super(RentalAdmin, self).save_model(request, obj, form, change)

admin.site.register(Rental,RentalAdmin)

class KindAdmin(admin.ModelAdmin):
	search_fields       = ['name','title']
	list_filter         = []
	list_display        = ('name','title','trans_time','handling_time','modified')
	readonly_fields     = ('created','modified','user')

	save_as             = True
	save_as_continue    = True
	save_on_top         = True

	fieldsets = [
		('Basic Information',{'fields': ['name','title','trans_time','handling_time']}),
		('System Information',{'fields':['user','created','modified']})
	]

	def save_model(self, request, obj, form, change):
		obj.user = request.user
		super(KindAdmin, self).save_model(request, obj, form, change)

admin.site.register(Kind,KindAdmin)


class CheResource(resources.ModelResource):
	class Meta:
		model = Che
		import_id_fields = ()
		skip_unchanged = True
		report_skipped= True
		fields = ('name','kind','title','created')

class CheAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['name','title']
	list_filter = ['kind']
	list_display = ('name','kind','title','created','modified')
	# list_editable = ('color','move_performa')
	readonly_fields = ('created','modified','user')

	save_as = True
	save_as_continue = True
	save_on_top =True

	fieldsets = [
		('Basic Information',{'fields': ['name','kind','title']}),
		('System Information',{'fields':['user','created','modified']})
	]
	resource_class      = CheResource

	def save_model(self, request, obj, form, change):
		obj.user = request.user
		super(CheAdmin, self).save_model(request, obj, form, change)

admin.site.register(Che,CheAdmin)


# Report
from .models import RentalDailySummary

@admin.register(RentalDailySummary)
class RentalSummaryAdmin(admin.ModelAdmin):
	change_list_template = 'admin/rental_summary_change_list.html'
	date_hierarchy = 'rent_date'
	# date_hierarchy_drilldown = False

	list_filter = (
		'terminal',
	)

	def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
		"""Drill-down only on past dates."""

		today = timezone.now().date()

		if year_lookup is None and month_lookup is None:
			# Past 3 years.
			# return (
			# 	datetime.date(y, 1, 1)
			# 	for y in range(today.year - 2, today.year + 1)
			# )
			return None

		elif year_lookup is not None and month_lookup is None:
			# Past months of selected year.
			this_month = today.replace(day=1)
			return (
				month for month in (
					datetime.date(int(year_lookup), month, 1)
					for month in range(1, 13)
				) if month <= this_month
			)

		elif year_lookup is not None and month_lookup is not None:
			# Past days of selected month.
			days_in_month = calendar.monthrange(year_lookup, month_lookup)[1]
			return (
				day for day in (
					datetime.date(year_lookup, month_lookup, i + 1)
					for i in range(days_in_month)
				) if day <= today
			)

	def changelist_view(self, request, extra_context=None):
		response = super().changelist_view(
			request,
			extra_context=extra_context,
		)

		try:
			qs = response.context_data['cl'].queryset
		except (AttributeError, KeyError):
			return response

		metrics = {
			'total_containers' : Count('container'),
			'total_handling_time' : Sum('che__kind__handling_time'),
			'transportation_time' : Max('che__kind__trans_time'),
			'total_minutes' : F('total_handling_time')+F('transportation_time'),
			'mod_minute' : Floor(F('total_minutes')/60),
			'total_hours' : Floor(F('total_minutes')/60)
		}
		reports     = qs.values('terminal','rent_date__date',
							'che__kind').annotate(
							**metrics).order_by(
							'terminal','rent_date__date',
							'che__kind'
							)
		
		for r in reports:
			mod_minute = r['total_minutes'] % 60
			hours   = math.floor(r['total_minutes'] / 60)
			hours   = hours + (0.5 if mod_minute > 0 and mod_minute < 30 else 0)
			hours   = hours + (1 if mod_minute >= 30 else 0)
			r['mod_minute'] = mod_minute
			r['total_hours'] = hours

		response.context_data['summary']=list(reports)
		return response

