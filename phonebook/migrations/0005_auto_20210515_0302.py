# Generated by Django 3.2.2 on 2021-05-14 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0004_auto_20210508_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='HP',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='country',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='gender',
        ),
    ]
