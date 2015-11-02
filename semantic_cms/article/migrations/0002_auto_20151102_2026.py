# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cover_image',
            field=models.ImageField(null=True, upload_to='images', blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='html',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='markdown',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(default='asdad'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='sub_title',
            field=models.CharField(default='sadad', max_length=128),
            preserve_default=False,
        ),
    ]
