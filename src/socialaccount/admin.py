from django.contrib import admin

from .models import SocialToken, SocialApp


class SocialTokenAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    search_fields = ('user__username', 'user__email',)
    list_display = ('user', 'app', 'truncated_token', 'created')
    list_filter = ('app', )

    def truncated_token(self, token):
        max_chars = 40
        ret = token.token
        if len(ret) > max_chars:
            ret = ret[0:max_chars] + '...(truncated)'
        return ret

    truncated_token.short_description = 'Token'


class SocialAppAdmin(admin.ModelAdmin):
    list_display = ('provider', 'name')


admin.site.register(SocialToken, SocialTokenAdmin)
admin.site.register(SocialApp, SocialAppAdmin)
