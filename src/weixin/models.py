#!/usr/bin/python
#  -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


WEIXIN_OPENACOUNT_TYPES = (
    ('subscribe', _(u'订阅号')),
    ('service', _(u'服务号')),
)


class PublicAccount(TimeStampedModel):
    user = models.ForeignKey(User)
    type = models.CharField(choices=WEIXIN_OPENACOUNT_TYPES, default='subscribe', max_length=10)
    title = models.CharField(max_length=255)
    winxin_id = models.CharField(max_length=255)
    thumbnail_url = models.URLField(blank=True, null=True)
    callback_url = models.URLField()
    token = models.CharField(max_length=255)
    connect_status = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s:%s' % (self.user, self.title)


class App(TimeStampedModel):
    title = models.CharField(max_length=255)
    thumbnail_url = models.URLField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(default=False)
    # TODO

    def __unicode__(self):
        return  self.title


class PublicAccountApp(TimeStampedModel):
    public_account = models.ForeignKey(PublicAccount)
    app = models.ForeignKey(App)

    def __unicode__(self):
        return  '%s:%s' % (self.public_account, self.app)


WEIXIN_MSG_TYPE = (
    ('text', _(u'Text')),
    ('image', _(u'Image')),
    ('voice', _(u'Voice')),
    ('video', _(u'Video')),
    ('location', _(u'Location')),
    ('link', _(u'Link')),
)


class Message(TimeStampedModel):
    public_account = models.ForeignKey(PublicAccount)
    to_user_name = models.CharField(max_length=255)
    from_user_name = models.CharField(max_length=255)
    create_time = models.BigIntegerField()
    msg_type = models.CharField(max_length=255, choices=WEIXIN_MSG_TYPE)
    msg_id = models.BigIntegerField()

    xml_content = models.TextField()


    def __unicode__(self):
        return self.msg_id


WEIXIN_EVENT_TYPE = (
    ('subscribe', _(u'subscribe')),
    ('unsubscribe', _(u'unsubscribe')),
    ('SCAN', _(u'SCAN')),
    ('LOCATION', _(u'LOCATION')),
    ('CLICK', _(u'CLICK')),
    ('VIEW', _(u'VIEW')),
)

class Event(TimeStampedModel):
    public_account = models.ForeignKey(PublicAccount)
    to_user_name = models.CharField(max_length=255)
    from_user_name = models.CharField(max_length=255)
    create_time = models.BigIntegerField()
    event_type = models.CharField(max_length=255, choices=WEIXIN_EVENT_TYPE)

    xml_content = models.TextField()


    def __unicode__(self):
        return self.event_type
