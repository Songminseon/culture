from django.contrib import admin
from .models import Content, Content_other
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin

class ContentAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

admin.site.register(Content, ContentAdmin)
admin.site.register(Content_other, ContentAdmin)
# Register your models here.
