# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-06 15:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flntr_app', '0002_auto_20180306_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
