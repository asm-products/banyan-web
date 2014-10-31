# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'StoryPermission', fields ['user', 'story']
        db.delete_unique(u'core_storypermission', ['user_id', 'story_id'])

        # Deleting model 'StoryPermission'
        db.delete_table(u'core_storypermission')

        # Adding model 'StoryGroupAccess'
        db.create_table(u'core_storygroupaccess', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('canRead', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('canWrite', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isInvited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lastUpdated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('createdAt', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Story'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['access_groups.AccessGroup'])),
        ))
        db.send_create_signal(u'core', ['StoryGroupAccess'])

        # Adding unique constraint on 'StoryGroupAccess', fields ['group', 'story']
        db.create_unique(u'core_storygroupaccess', ['group_id', 'story_id'])

        # Adding model 'StoryUserAccess'
        db.create_table(u'core_storyuseraccess', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('canRead', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('canWrite', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isInvited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lastUpdated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('createdAt', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Story'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.BanyanUser'])),
        ))
        db.send_create_signal(u'core', ['StoryUserAccess'])

        # Adding unique constraint on 'StoryUserAccess', fields ['user', 'story']
        db.create_unique(u'core_storyuseraccess', ['user_id', 'story_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'StoryUserAccess', fields ['user', 'story']
        db.delete_unique(u'core_storyuseraccess', ['user_id', 'story_id'])

        # Removing unique constraint on 'StoryGroupAccess', fields ['group', 'story']
        db.delete_unique(u'core_storygroupaccess', ['group_id', 'story_id'])

        # Adding model 'StoryPermission'
        db.create_table(u'core_storypermission', (
            ('isValid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.BanyanUser'])),
            ('canWrite', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('canRead', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Story'])),
            ('isInvited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lastUpdated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['StoryPermission'])

        # Adding unique constraint on 'StoryPermission', fields ['user', 'story']
        db.create_unique(u'core_storypermission', ['user_id', 'story_id'])

        # Deleting model 'StoryGroupAccess'
        db.delete_table(u'core_storygroupaccess')

        # Deleting model 'StoryUserAccess'
        db.delete_table(u'core_storyuseraccess')


    models = {
        u'access_groups.accessgroup': {
            'Meta': {'unique_together': "(('groupdesc_content_type', 'groupdesc_object_id'),)", 'object_name': 'AccessGroup'},
            'groupdesc_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'groupdesc_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'access_groups'", 'to': u"orm['accounts.BanyanUser']", 'through': u"orm['access_groups.GroupMembership']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        u'access_groups.groupmembership': {
            'Meta': {'unique_together': "(('group', 'user'),)", 'object_name': 'GroupMembership'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': u"orm['access_groups.AccessGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': u"orm['accounts.BanyanUser']"})
        },
        u'accounts.banyanuser': {
            'Meta': {'object_name': 'BanyanUser'},
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.activity': {
            'Meta': {'unique_together': "(('user', 'object_id', 'content_type', 'type'),)", 'object_name': 'Activity'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'createdAt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.BanyanUser']", 'null': 'True', 'blank': 'True'})
        },
        u'core.piece': {
            'Meta': {'ordering': "['timeStamp']", 'object_name': 'Piece'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'core_piece_author'", 'to': u"orm['accounts.BanyanUser']"}),
            'bnObjectId': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'contributors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'core_piece_contributors'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.BanyanUser']"}),
            'createdAt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'isLocationEnabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'longText': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'media': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'shortText': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pieces'", 'to': u"orm['core.Story']"}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'timeStamp': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'updatedAt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.story': {
            'Meta': {'ordering': "['-timeStamp']", 'object_name': 'Story'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'core_story_author'", 'to': u"orm['accounts.BanyanUser']"}),
            'bnObjectId': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'contributors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'core_story_contributors'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.BanyanUser']"}),
            'createdAt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'isLocationEnabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'media': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'permittedGroups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'stories'", 'to': u"orm['access_groups.AccessGroup']", 'through': u"orm['core.StoryGroupAccess']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'permittedUsers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'stories'", 'to': u"orm['accounts.BanyanUser']", 'through': u"orm['core.StoryUserAccess']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'readAccess': ('jsonfield.fields.JSONField', [], {}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'timeStamp': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updatedAt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'writeAccess': ('jsonfield.fields.JSONField', [], {})
        },
        u'core.storygroupaccess': {
            'Meta': {'unique_together': "(('group', 'story'),)", 'object_name': 'StoryGroupAccess'},
            'canRead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'canWrite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'createdAt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['access_groups.AccessGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isInvited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lastUpdated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Story']"})
        },
        u'core.storyuseraccess': {
            'Meta': {'unique_together': "(('user', 'story'),)", 'object_name': 'StoryUserAccess'},
            'canRead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'canWrite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'createdAt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isInvited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lastUpdated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.BanyanUser']"})
        }
    }

    complete_apps = ['core']