# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-17 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_bundle_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='bundle',
            name='source_url',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]