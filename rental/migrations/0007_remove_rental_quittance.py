# Generated by Django 2.2.1 on 2019-05-24 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0006_auto_20190523_2337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rental',
            name='quittance',
        ),
    ]
