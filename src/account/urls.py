from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns("",
                       url(r"^confirm_email/(?P<key>\w+)/$", views.confirm_email, name="account_confirm_email"),
                       url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", views.password_reset_from_key,
                           name="account_reset_password_from_key"),
                       url(r'^password/reset/success/$', 'account.views.reset_password_done',
                           name='reset_password_done'),
)
