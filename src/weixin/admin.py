from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.contenttypes.generic import GenericTabularInline

from attachment.models import AttachmentRelationship
from .models import PublicAccount, Message, Event, PublicAccountApp, App


class AppInline(TabularInline):
    model = PublicAccountApp


class PublicAccountAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    inlines = [
        AppInline,
    ]


class AvatarPhotoAdmin(admin.ModelAdmin):
    list_display = ('photo', 'created',)


class MessageAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('from_user_name', 'msg_id', 'to_user_name', 'msg_type', 'create_time', 'public_account', 'created')
    search_fields = ('from_user_name',)


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('from_user_name', 'event_type', 'to_user_name', 'create_time', 'public_account', 'created')
    search_fields = ('from_user_name',)


class AttachmentInline(GenericTabularInline):
    model = AttachmentRelationship


class WeixinAppAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('title', 'version', 'source', 'description', 'creator', 'created')
    search_fields = ('title', 'description')
    inlines = [
        AttachmentInline,
    ]


admin.site.register(Message, MessageAdmin)
admin.site.register(Event, EventAdmin)

admin.site.register(PublicAccount, PublicAccountAdmin)
admin.site.register(App, WeixinAppAdmin)
