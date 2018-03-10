# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-10 19:30
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('numberOfRooms', models.IntegerField()),
                ('streetAddress', models.CharField(max_length=64)),
                ('postCode', models.CharField(max_length=8)),
                ('description', models.TextField(blank=True)),
                ('averageRoomPrice', models.DecimalField(decimal_places=2, max_digits=6)),
                ('slug', models.SlugField(unique=True)),
                ('dayAdded', models.DateField(default=datetime.datetime.now)),
                ('views', models.IntegerField(default=0)),
                ('distanceFromUniversity', models.IntegerField(default=0)),
                ('distanceText', models.CharField(default='0 mi', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='FlatImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageNumber', models.IntegerField()),
                ('image', models.ImageField(blank=True, upload_to='flat_images')),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='flntr_app.Flat')),
            ],
        ),
        migrations.CreateModel(
            name='Landlord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomNumber', models.IntegerField()),
                ('size', models.CharField(max_length=8)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flntr_app.Flat')),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('bio', models.TextField(blank=True)),
                ('age', models.IntegerField(default=0)),
                ('gender', models.CharField(max_length=10)),
                ('slug', models.SlugField(unique=True)),
                ('properties', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flntr_app.Flat')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='student',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flntr_app.StudentProfile'),
        ),
        migrations.AddField(
            model_name='flat',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flntr_app.Landlord'),
        ),
    ]
