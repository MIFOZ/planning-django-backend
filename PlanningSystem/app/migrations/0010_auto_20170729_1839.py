# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 12:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20170729_1607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='workflow',
            new_name='business_process',
        ),
    ]
