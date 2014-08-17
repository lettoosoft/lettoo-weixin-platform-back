from django.conf.urls import patterns, url


urlpatterns = patterns('weixin.views',
                       url(r'^weixin/(?P<user_id>\d+)/(?P<token>\w+)/$', 'weixin', name='weixin'),
)
