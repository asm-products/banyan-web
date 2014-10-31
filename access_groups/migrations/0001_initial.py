# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AccessGroup'
        db.create_table(u'access_groups_accessgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('groupdesc_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('groupdesc_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'access_groups', ['AccessGroup'])

        # Adding unique constraint on 'AccessGroup', fields ['groupdesc_content_type', 'groupdesc_object_id']
        db.create_unique(u'access_groups_accessgroup', ['groupdesc_content_type_id', 'groupdesc_object_id'])

        # Adding model 'GroupMembership'
        db.create_table(u'access_groups_groupmembership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberships', to=orm['access_groups.AccessGroup'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberships', to=orm['accounts.BanyanUser'])),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'access_groups', ['GroupMembership'])

        # Adding unique constraint on 'GroupMembership', fields ['group', 'user']
        db.create_unique(u'access_groups_groupmembership', ['group_id', 'user_id'])

        # Adding model 'SoloGroupDesc'
        db.create_table(u'access_groups_sologroupdesc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('user_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'access_groups', ['SoloGroupDesc'])

        # Adding model 'FbFriendOfGroupDesc'
        db.create_table(u'access_groups_fbfriendofgroupdesc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'access_groups', ['FbFriendOfGroupDesc'])

        # Adding model 'PublicGroupDesc'
        db.create_table(u'access_groups_publicgroupdesc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'access_groups', ['PublicGroupDesc'])


    def backwards(self, orm):
        # Removing unique constraint on 'GroupMembership', fields ['group', 'user']
        db.delete_unique(u'access_groups_groupmembership', ['group_id', 'user_id'])

        # Removing unique constraint on 'AccessGroup', fields ['groupdesc_content_type', 'groupdesc_object_id']
        db.delete_unique(u'access_groups_accessgroup', ['groupdesc_content_type_id', 'groupdesc_object_id'])

        # Deleting model 'AccessGroup'
        db.delete_table(u'access_groups_accessgroup')

        # Deleting model 'GroupMembership'
        db.delete_table(u'access_groups_groupmembership')

        # Deleting model 'SoloGroupDesc'
        db.delete_table(u'access_groups_sologroupdesc')

        # Deleting model 'FbFriendOfGroupDesc'
        db.delete_table(u'access_groups_fbfriendofgroupdesc')

        # Deleting model 'PublicGroupDesc'
        db.delete_table(u'access_groups_publicgroupdesc')


    models = {
        u'access_groups.accessgroup': {
            'Meta': {'unique_together': "(('groupdesc_content_type', 'groupdesc_object_id'),)", 'object_name': 'AccessGroup'},
            'groupdesc_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'groupdesc_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'access_groups'", 'to': u"orm['accounts.BanyanUser']", 'through': u"orm['access_groups.GroupMembership']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        u'access_groups.fbfriendofgroupdesc': {
            'Meta': {'object_name': 'FbFriendOfGroupDesc'},
            'fb_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'access_groups.groupmembership': {
            'Meta': {'unique_together': "(('group', 'user'),)", 'object_name': 'GroupMembership'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': u"orm['access_groups.AccessGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': u"orm['accounts.BanyanUser']"})
        },
        u'access_groups.publicgroupdesc': {
            'Meta': {'object_name': 'PublicGroupDesc'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'access_groups.sologroupdesc': {
            'Meta': {'object_name': 'SoloGroupDesc'},
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['access_groups']