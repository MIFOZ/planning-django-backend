# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 08:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170729_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='app.StructureUnit'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='default_deputy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='app.Employee'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='deputy_by_order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='app.Employee'),
        ),
    ]