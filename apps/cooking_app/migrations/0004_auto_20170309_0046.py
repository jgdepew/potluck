# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 00:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooking_app', '0003_auto_20170309_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='cooking_app.Recipe'),
        ),
    ]
