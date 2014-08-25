from django.contrib import admin

from .models import Attachment


class AttachmentAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    raw_id_fields = ('user',)
    list_display = ('name', 'user', 'file',  'created')


admin.site.register(Attachment, AttachmentAdmin)
