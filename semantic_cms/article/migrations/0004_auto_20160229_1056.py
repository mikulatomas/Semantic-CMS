# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-29 09:56
from __future__ import unicode_literals

from django.db import migrations
import imagekit.models.fields
import semantic_cms.image_tools


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20160227_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='cover_image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=semantic_cms.image_tools.upload_to_id_image),
        ),
    ]