# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-07 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dumpsters", "0002_dumpster_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voting",
            name="comment",
            field=models.CharField(max_length=2000),
        ),
    ]
