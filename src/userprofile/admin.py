from django.contrib import admin

from .models import Profile, AvatarPhoto


class ProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('user', 'extra_data', 'created', 'modified')


class AvatarPhotoAdmin(admin.ModelAdmin):
    list_display = ('photo', 'created',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(AvatarPhoto, AvatarPhotoAdmin)
