# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 00:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooking_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipepic',
            name='recipe',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_image', to='cooking_app.Recipe'),
        ),
    ]
