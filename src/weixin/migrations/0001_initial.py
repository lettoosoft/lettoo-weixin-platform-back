# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PublicAccount'
        db.create_table(u'weixin_publicaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='subscribe', max_length=10)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('thumbnail_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('callback_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('connect_status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'weixin', ['PublicAccount'])

        # Adding model 'App'
        db.create_table(u'weixin_app', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('thumbnail_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'weixin', ['App'])

        # Adding model 'PublicAccountApp'
        db.create_table(u'weixin_publicaccountapp', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('public_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weixin.PublicAccount'])),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weixin.App'])),
        ))
        db.send_create_signal(u'weixin', ['PublicAccountApp'])

        # Adding model 'Message'
        db.create_table(u'weixin_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('public_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weixin.PublicAccount'])),
            ('to_user_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('from_user_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('create_time', self.gf('django.db.models.fields.BigIntegerField')()),
            ('msg_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('msg_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('xml_content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'weixin', ['Message'])

        # Adding model 'Event'
        db.create_table(u'weixin_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('public_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weixin.PublicAccount'])),
            ('to_user_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('from_user_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('create_time', self.gf('django.db.models.fields.BigIntegerField')()),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('xml_content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'weixin', ['Event'])


    def backwards(self, orm):
        # Deleting model 'PublicAccount'
        db.delete_table(u'weixin_publicaccount')

        # Deleting model 'App'
        db.delete_table(u'weixin_app')

        # Deleting model 'PublicAccountApp'
        db.delete_table(u'weixin_publicaccountapp')

        # Deleting model 'Message'
        db.delete_table(u'weixin_message')

        # Deleting model 'Event'
        db.delete_table(u'weixin_event')


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
        u'weixin.app': {
            'Meta': {'object_name': 'App'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'thumbnail_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'weixin.event': {
            'Meta': {'object_name': 'Event'},
            'create_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'from_user_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'public_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weixin.PublicAccount']"}),
            'to_user_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'xml_content': ('django.db.models.fields.TextField', [], {})
        },
        u'weixin.message': {
            'Meta': {'object_name': 'Message'},
            'create_time': ('django.db.models.fields.BigIntegerField', [], {}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'from_user_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'msg_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'msg_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'public_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weixin.PublicAccount']"}),
            'to_user_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'xml_content': ('django.db.models.fields.TextField', [], {})
        },
        u'weixin.publicaccount': {
            'Meta': {'object_name': 'PublicAccount'},
            'callback_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'connect_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'thumbnail_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'subscribe'", 'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'weixin.publicaccountapp': {
            'Meta': {'object_name': 'PublicAccountApp'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weixin.App']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'public_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weixin.PublicAccount']"})
        }
    }

    complete_apps = ['weixin']