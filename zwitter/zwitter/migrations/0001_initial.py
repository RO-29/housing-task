# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import zwitter.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('fs_id', models.AutoField(serialize=False, primary_key=True)),
                ('follower_id', models.IntegerField(verbose_name=zwitter.models.Users)),
                ('since', models.DateTimeField(verbose_name=b'Followed on')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('fg_id', models.AutoField(serialize=False, primary_key=True)),
                ('following_id', models.IntegerField(verbose_name=zwitter.models.Users)),
                ('since', models.DateTimeField(verbose_name=b'Following on')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('hid', models.AutoField(serialize=False, primary_key=True)),
                ('hash_name', models.CharField(max_length=160)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tweets',
            fields=[
                ('tid', models.AutoField(serialize=False, primary_key=True)),
                ('posted', models.DateTimeField(verbose_name=b'Followed on')),
                ('tweet', models.TextField(max_length=160)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('uid', models.AutoField(serialize=False, primary_key=True)),
                ('fname', models.CharField(max_length=250)),
                ('lname', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=500)),
                ('handle', models.CharField(unique=True, max_length=100)),
                ('password', models.CharField(max_length=250)),
                ('about', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tweets',
            name='uid',
            field=models.ForeignKey(to='zwitter.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hashtag',
            name='tid',
            field=models.ForeignKey(to='zwitter.Tweets'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='following',
            name='uid',
            field=models.ForeignKey(to='zwitter.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='followers',
            name='uid',
            field=models.ForeignKey(to='zwitter.Users'),
            preserve_default=True,
        ),
    ]
