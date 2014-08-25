from django.conf.urls import patterns, url


urlpatterns = patterns('attachment.views',
                       url(r'^upload/$', 'attachment_upload', name='attachment_upload'),
)