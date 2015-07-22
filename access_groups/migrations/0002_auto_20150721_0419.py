# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('access_groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmembership',
            name='user',
            field=models.ForeignKey(related_name='memberships', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accessgroup',
            name='groupdesc_content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='accessgroup',
            name='users',
            field=models.ManyToManyField(related_name='access_groups', through='access_groups.GroupMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='groupmembership',
            unique_together=set([('group', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='accessgroup',
            unique_together=set([('groupdesc_content_type', 'groupdesc_object_id')]),
        ),
    ]
