# Generated by Django 2.2.1 on 2019-05-17 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0002_auto_20190517_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bedroom',
            name='superficy',
            field=models.DecimalField(decimal_places=0, max_digits=3),
        ),
    ]
