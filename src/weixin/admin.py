from django.contrib import admin

from .models import PublicAccount, Message, Event


class PublicAccountAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('weixin_id', 'title', 'type', 'callback_url', 'token', 'user', 'created', 'modified')


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


admin.site.register(Message, MessageAdmin)
admin.site.register(Event, EventAdmin)

admin.site.register(PublicAccount, PublicAccountAdmin)
