# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-25 12:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Landlord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=32)),
                ('sname', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flntr_app.Landlord')),
            ],
        ),
        migrations.CreateModel(
            name='RoomDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('description', models.TextField(blank=True)),
                ('room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='flntr_app.Room')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=32)),
                ('sname', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('bio', models.TextField(blank=True)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='flntr_app.Student')),
            ],
        ),
    ]