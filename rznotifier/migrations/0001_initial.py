# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-19 07:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.IntegerField(db_index=True)),
                ('date_published', models.DateTimeField()),
                ('main_income_type', models.CharField(max_length=30)),
                ('region', models.SmallIntegerField()),
                ('rating', models.CharField(db_index=True, max_length=5)),
                ('nick_name', models.CharField(max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
