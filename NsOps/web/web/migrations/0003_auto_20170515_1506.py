# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-15 07:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_usertype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='email',
            new_name='Email',
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='username',
            new_name='Username',
        ),
        migrations.RenameField(
            model_name='usertype',
            old_name='name',
            new_name='Name',
        ),
    ]
