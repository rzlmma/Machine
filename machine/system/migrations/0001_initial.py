# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.CharField(max_length=128, null=True, blank=True)),
                ('real_name', models.CharField(max_length=128, null=True, blank=True)),
                ('position', models.CharField(max_length=128, null=True, blank=True)),
                ('gender', models.CharField(default=b'SECRECY', max_length=16, null=True, blank=True, choices=[(b'\xe7\x94\xb7', b'male'), (b'\xe5\xa5\xb3', b'female'), (b'\xe4\xbf\x9d\xe5\xaf\x86', b'secrecy')])),
                ('phone', models.CharField(max_length=64, null=True, blank=True)),
                ('mobile', models.CharField(max_length=64, null=True, blank=True)),
                ('status', models.BooleanField(default=True)),
                ('leader_id', models.CharField(max_length=64, null=True, blank=True)),
                ('dept_id', models.CharField(max_length=64, null=True, blank=True)),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
            ],
            options={
                'abstract': False,
                'db_table': 'user',
                'verbose_name': '\u7528\u6237',
                'swappable': 'AUTH_USER_MODEL',
                'verbose_name_plural': '\u7528\u6237',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('parent_id', models.IntegerField(null=True, blank=True)),
                ('manager', models.CharField(max_length=128, null=True, blank=True)),
                ('comment', models.CharField(max_length=128, null=True, blank=True)),
                ('created_time', models.TimeField(null=True, blank=True)),
                ('updated_time', models.TimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'department',
                'verbose_name': '\u90e8\u95e8',
                'verbose_name_plural': '\u90e8\u95e8',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('codename', models.CharField(unique=True, max_length=100, verbose_name='Codename')),
            ],
            options={
                'db_table': 'permission',
                'verbose_name': '\u6743\u9650',
                'verbose_name_plural': '\u6743\u9650',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('codename', models.CharField(unique=True, max_length=128)),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'role',
                'verbose_name': '\u89d2\u8272',
                'verbose_name_plural': '\u89d2\u8272',
            },
        ),
        migrations.CreateModel(
            name='RolePermissionRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.ForeignKey(verbose_name='Permission', to='system.Permission')),
                ('role', models.ForeignKey(verbose_name='Role', blank=True, to='system.Role', null=True)),
            ],
            options={
                'ordering': ('role',),
                'db_table': 'role_permission_relation',
                'verbose_name': '\u89d2\u8272-\u6743\u9650',
                'verbose_name_plural': '\u89d2\u8272-\u6743\u9650',
            },
        ),
        migrations.CreateModel(
            name='UserRoleRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.ForeignKey(verbose_name='Role', to='system.Role')),
                ('user', models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('user',),
                'db_table': 'user_role_relation',
                'verbose_name': '\u7528\u6237-\u89d2\u8272',
                'verbose_name_plural': '\u7528\u6237-\u89d2\u8272',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
