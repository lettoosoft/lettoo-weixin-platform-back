#!/usr/bin/python
# -*- coding: utf-8 -*-
from uuid import uuid4

from attachment.models import AttachmentRelationship
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager


WEIXIN_OPENACOUNT_TYPES = (
    ('subscribe', u'订阅号'),
    ('service', u'服务号'),
)


class PublicAccount(TimeStampedModel):
    user = models.ForeignKey(User)
    type = models.CharField(choices=WEIXIN_OPENACOUNT_TYPES, default=u'subscribe', max_length=10)
    title = models.CharField(max_length=255)
    weixin_id = models.CharField(max_length=255)
    thumbnail_url = models.URLField(blank=True, null=True)
    callback_url = models.URLField()
    token = models.CharField(max_length=255)
    connect_status = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s:%s' % (self.user, self.title)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.token == None:
            token = uuid4().hex
            self.token = token
        if self.callback_url == None:
            callback_url = '/weixin/%d/%s/' % (self.user.id, token)
            request = HttpRequest()
            self.callback_url =request.build_absolute_uri(callback_url)
        super(PublicAccount, self).save(force_insert, force_update, using, update_fields)


class App(TimeStampedModel):
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    full_description = models.TextField(null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)
    version = models.CharField(max_length=255)
    source = models.CharField(max_length=255, default=u'官方', null=True, blank=True)
    need_paid = models.BooleanField(default=False)
    price = models.FloatField(default=0.0)
    rate = models.FloatField(default=5.0)
    install_count = models.PositiveIntegerField(default=0)
    keywords = TaggableManager()
    published = models.BooleanField(default=False)

    @property
    def attachments(self):
        return [item.json for item in AttachmentRelationship.objects.filter_attachment(self)]

    def __unicode__(self):
        return self.title


class PublicAccountApp(TimeStampedModel):
    public_account = models.ForeignKey(PublicAccount)
    app = models.ForeignKey(App)

    def __unicode__(self):
        return u'%s:%s' % (self.public_account, self.app)


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
