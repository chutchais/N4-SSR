from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

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
