from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
# Register your models here.
from .models import Department,Ssr,Ssrfiles

class DepartmentAdmin(admin.ModelAdmin):
    search_fields       = ['name','description']
    list_filter         = []
    list_display        = ('name','description','created','modified')
    readonly_fields     = ('created','modified','user')

    save_as             = True
    save_as_continue    = True
    save_on_top         = True

    fieldsets = [
        ('Basic Information',{'fields': ['name','description']}),
        ('System Information',{'fields':['user','created','modified']})
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(DepartmentAdmin, self).save_model(request, obj, form, change)

admin.site.register(Department,DepartmentAdmin)


class SsrFileInline(admin.TabularInline):
	model = Ssrfiles
	fields = ['file','note']
	extra = 0

class SsrAdmin(admin.ModelAdmin):
    search_fields       = ['number','title','note']
    list_filter         = ['completed','department']
    list_display        = ('number','title','department','total_file','created','modified','completed')
    readonly_fields     = ('created','modified','user')
    # readonly_fields     = ('number','created','modified','user')

    save_as             = True
    save_as_continue    = True
    save_on_top         = True

    fieldsets = [
        ('Basic Information',{'fields': [('number','completed'),'title','department',
        						'note']}),
        ('System Information',{'fields':['user','created','modified']})
    ]
    inlines = [SsrFileInline]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(SsrAdmin, self).save_model(request, obj, form, change)

admin.site.register(Ssr,SsrAdmin)