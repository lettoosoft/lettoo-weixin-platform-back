from django.contrib import admin

from .models import PublicAccount


class PublicAccountAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('weixin_id', 'title', 'type', 'callback_url', 'token', 'user', 'created', 'modified')


class AvatarPhotoAdmin(admin.ModelAdmin):
    list_display = ('photo', 'created',)


admin.site.register(PublicAccount, PublicAccountAdmin)
