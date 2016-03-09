# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-25 13:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import keywords.managers
import redactor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flags', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('semantic', '__first__'),
        ('keywords', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('sub_title', models.CharField(blank=True, max_length=128, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('status', models.CharField(choices=[('D', 'Draft'), ('P', 'Published')], default='D', max_length=1)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='articles/')),
                ('content', redactor.fields.RedactorField(verbose_name='Content')),
                ('edited_date', models.DateTimeField(blank=True, null=True, verbose_name='date edited')),
                ('created_date', models.DateTimeField(verbose_name='date created')),
                ('published_date', models.DateTimeField(blank=True, null=True, verbose_name='date published')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('flag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flags.Flag')),
                ('keywords', keywords.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='keywords.TaggedArticle', to='keywords.Keyword', verbose_name='Tags')),
                ('semantic', models.ManyToManyField(blank=True, to='semantic.Semantic')),
            ],
            options={
                'ordering': ['created_date'],
                'get_latest_by': 'published_date',
            },
        ),
    ]