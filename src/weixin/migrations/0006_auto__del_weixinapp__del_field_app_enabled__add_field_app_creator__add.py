# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'WeixinApp'
        db.delete_table(u'weixin_weixinapp')

        # Deleting field 'App.enabled'
        db.delete_column(u'weixin_app', 'enabled')

        # Adding field 'App.creator'
        db.add_column(u'weixin_app', 'creator',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'App.full_description'
        db.add_column(u'weixin_app', 'full_description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'App.version'
        db.add_column(u'weixin_app', 'version',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'App.source'
        db.add_column(u'weixin_app', 'source',
                      self.gf('django.db.models.fields.CharField')(default=u'\u5b98\u65b9', max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'App.need_paid'
        db.add_column(u'weixin_app', 'need_paid',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'App.price'
        db.add_column(u'weixin_app', 'price',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'App.rate'
        db.add_column(u'weixin_app', 'rate',
                      self.gf('django.db.models.fields.FloatField')(default=5.0),
                      keep_default=False)

        # Adding field 'App.install_count'
        db.add_column(u'weixin_app', 'install_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'App.published'
        db.add_column(u'weixin_app', 'published',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'WeixinApp'
        db.create_table(u'weixin_weixinapp', (
            ('install_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('price', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('full_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rate', self.gf('django.db.models.fields.FloatField')(default=5.0)),
            ('thumbnail_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('need_paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('source', self.gf('django.db.models.fields.CharField')(default=u'\u5b98\u65b9', max_length=255, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'weixin', ['WeixinApp'])

        # Adding field 'App.enabled'
        db.add_column(u'weixin_app', 'enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'App.creator'
        db.delete_column(u'weixin_app', 'creator_id')

        # Deleting field 'App.full_description'
        db.delete_column(u'weixin_app', 'full_description')

        # Deleting field 'App.version'
        db.delete_column(u'weixin_app', 'version')

        # Deleting field 'App.source'
        db.delete_column(u'weixin_app', 'source')

        # Deleting field 'App.need_paid'
        db.delete_column(u'weixin_app', 'need_paid')

        # Deleting field 'App.price'
        db.delete_column(u'weixin_app', 'price')

        # Deleting field 'App.rate'
        db.delete_column(u'weixin_app', 'rate')

        # Deleting field 'App.install_count'
        db.delete_column(u'weixin_app', 'install_count')

        # Deleting field 'App.published'
        db.delete_column(u'weixin_app', 'published')


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
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'full_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'install_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'need_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rate': ('django.db.models.fields.FloatField', [], {'default': '5.0'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "u'\\u5b98\\u65b9'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'thumbnail_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'thumbnail_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'subscribe'", 'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'weixin_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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