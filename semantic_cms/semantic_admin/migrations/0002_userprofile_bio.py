# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-04 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('semantic_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
