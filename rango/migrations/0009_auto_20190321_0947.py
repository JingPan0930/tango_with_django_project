# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-21 01:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0008_auto_20190320_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postad',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]