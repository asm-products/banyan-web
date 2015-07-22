# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
        ('accounts', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banyanusernotifications',
            name='activity',
            field=models.ForeignKey(blank=True, to='core.Activity', null=True),
        ),
        migrations.AddField(
            model_name='banyanusernotifications',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='banyanusernotifications',
            name='from_user',
            field=models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='banyanusernotifications',
            name='user',
            field=models.ForeignKey(related_name='notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='banyanuserdevices',
            name='user',
            field=models.ForeignKey(related_name='installations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='banyanuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='banyanuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='banyanusernotifications',
            unique_together=set([('user', 'from_user', 'object_id', 'content_type', 'type')]),
        ),
    ]
