# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SocialApp'
        db.create_table(u'socialaccount_socialapp', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('provider', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('client_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'socialaccount', ['SocialApp'])

        # Adding model 'SocialToken'
        db.create_table(u'socialaccount_socialtoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['socialaccount.SocialApp'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token', self.gf('encrypted_fields.fields.EncryptedTextField')()),
            ('token_secret', self.gf('encrypted_fields.fields.EncryptedTextField')(blank=True)),
            ('expires', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('extra_data', self.gf('jsonfield.fields.JSONField')(default='{}')),
        ))
        db.send_create_signal(u'socialaccount', ['SocialToken'])

        # Adding unique constraint on 'SocialToken', fields ['app', 'user']
        db.create_unique(u'socialaccount_socialtoken', ['app_id', 'user_id'])

        # Adding model 'GooglePushNotification'
        db.create_table(u'socialaccount_googlepushnotification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('channel_id', self.gf('django.db.models.fields.CharField')(default='54e11190987136156036c10e04fdcb617c12b117', max_length=256)),
            ('resourceId', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('expiration', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'socialaccount', ['GooglePushNotification'])


    def backwards(self, orm):
        # Removing unique constraint on 'SocialToken', fields ['app', 'user']
        db.delete_unique(u'socialaccount_socialtoken', ['app_id', 'user_id'])

        # Deleting model 'SocialApp'
        db.delete_table(u'socialaccount_socialapp')

        # Deleting model 'SocialToken'
        db.delete_table(u'socialaccount_socialtoken')

        # Deleting model 'GooglePushNotification'
        db.delete_table(u'socialaccount_googlepushnotification')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'socialaccount.googlepushnotification': {
            'Meta': {'object_name': 'GooglePushNotification'},
            'channel_id': ('django.db.models.fields.CharField', [], {'default': "'22ea33ed27e3046b1eff8596026db9a475c60dfb'", 'max_length': '256'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'expiration': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'resourceId': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'socialaccount.socialapp': {
            'Meta': {'object_name': 'SocialApp'},
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'provider': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'socialaccount.socialtoken': {
            'Meta': {'unique_together': "(('app', 'user'),)", 'object_name': 'SocialToken'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['socialaccount.SocialApp']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'expires': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'extra_data': ('jsonfield.fields.JSONField', [], {'default': "'{}'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'token': ('encrypted_fields.fields.EncryptedTextField', [], {}),
            'token_secret': ('encrypted_fields.fields.EncryptedTextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['socialaccount']