# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('slug', models.SlugField()),
                ('edited_date', models.DateTimeField(verbose_name='date edited', blank=True, null=True)),
                ('created_date', models.DateTimeField(verbose_name='date created')),
            ],
            options={
                'get_latest_by': 'created_date',
                'ordering': ['name'],
            },
        ),
    ]
