# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('access_groups', '0002_auto_20150721_0419'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField(db_index=True)),
                ('type', models.CharField(db_index=True, max_length=20, choices=[(b'like', b'like'), (b'followUser', b'following user'), (b'followStory', b'following story'), (b'view', b'view')])),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Piece',
            fields=[
                ('bnObjectId', models.AutoField(serialize=False, primary_key=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('isLocationEnabled', models.BooleanField(default=False)),
                ('location', jsonfield.fields.JSONField(null=True, blank=True)),
                ('timeStamp', models.IntegerField(db_index=True)),
                ('tags', models.CharField(max_length=500, null=True, blank=True)),
                ('shortText', models.TextField(null=True, blank=True)),
                ('longText', models.TextField(null=True, blank=True)),
                ('media', jsonfield.fields.JSONField(null=True, blank=True)),
                ('author', models.ForeignKey(related_name='core_piece_author', to=settings.AUTH_USER_MODEL)),
                ('contributors', models.ManyToManyField(related_name='core_piece_contributors', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['timeStamp'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('bnObjectId', models.AutoField(serialize=False, primary_key=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('isLocationEnabled', models.BooleanField(default=False)),
                ('location', jsonfield.fields.JSONField(null=True, blank=True)),
                ('timeStamp', models.IntegerField(db_index=True)),
                ('tags', models.CharField(max_length=500, null=True, blank=True)),
                ('title', models.CharField(max_length=200)),
                ('readAccess', jsonfield.fields.JSONField()),
                ('writeAccess', jsonfield.fields.JSONField()),
                ('media', jsonfield.fields.JSONField(null=True, blank=True)),
                ('author', models.ForeignKey(related_name='core_story_author', to=settings.AUTH_USER_MODEL)),
                ('contributors', models.ManyToManyField(related_name='core_story_contributors', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timeStamp'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoryGroupAccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('canRead', models.BooleanField(default=False)),
                ('canWrite', models.BooleanField(default=False)),
                ('isInvited', models.BooleanField(default=False)),
                ('lastUpdated', models.DateTimeField(auto_now=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(to='access_groups.AccessGroup')),
                ('story', models.ForeignKey(to='core.Story')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoryUserAccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('canRead', models.BooleanField(default=False)),
                ('canWrite', models.BooleanField(default=False)),
                ('isInvited', models.BooleanField(default=False)),
                ('lastUpdated', models.DateTimeField(auto_now=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('story', models.ForeignKey(to='core.Story')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='story',
            name='permittedGroups',
            field=models.ManyToManyField(related_name='stories', through='core.StoryGroupAccess', to='access_groups.AccessGroup'),
        ),
        migrations.AddField(
            model_name='story',
            name='permittedUsers',
            field=models.ManyToManyField(related_name='stories', through='core.StoryUserAccess', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='piece',
            name='story',
            field=models.ForeignKey(related_name='pieces', to='core.Story'),
        ),
        migrations.AlterUniqueTogether(
            name='storyuseraccess',
            unique_together=set([('user', 'story')]),
        ),
        migrations.AlterUniqueTogether(
            name='storygroupaccess',
            unique_together=set([('group', 'story')]),
        ),
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together=set([('user', 'object_id', 'content_type', 'type')]),
        ),
    ]
