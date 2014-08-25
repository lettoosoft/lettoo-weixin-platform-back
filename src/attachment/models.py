from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from sorl.thumbnail import get_thumbnail
from model_utils.models import TimeStampedModel

from .utils import get_attachment_filename
from .managers import AttachmentRelationshipManager


class Attachment(TimeStampedModel):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to=get_attachment_filename)

    def __unicode__(self):
        return self.name

    @property
    def file_type(self):
        ext = self.file.name.split('.')[-1]
        return ext

    @property
    def json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'file_type': self.file_type,
            'url': self.file.url,
        }
        return data

    def get_thumbnail(self, size):
        '''
        get thumbnail from a size (width, height)
        :param size: (width, height)
        :return:
        '''
        return get_thumbnail(self.file, '%sx%s' % size, quality=99)


class AttachmentRelationship(TimeStampedModel):
    # Content-object field
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey(ct_field='content_type', fk_field='object_id')

    # Metadata about the attachment
    attachment = models.ForeignKey(Attachment)

    # Manager
    objects = AttachmentRelationshipManager()
