# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=256, null=True, blank=True)),
                ('photo_link', models.CharField(max_length=128)),
                ('favor_cnt', models.IntegerField(default=0, null=True)),
                ('dislike_cnt', models.IntegerField(default=0, null=True)),
                ('upload_time', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-upload_time',),
                'db_table': 'photo',
                'verbose_name': '\u7167\u7247',
                'verbose_name_plural': '\u7167\u7247',
            },
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=256, null=True, blank=True)),
                ('create_time', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('create_time',),
                'db_table': 'remark',
                'verbose_name': '\u7167\u7247',
                'verbose_name_plural': '\u7167\u7247',
            },
        ),
    ]
