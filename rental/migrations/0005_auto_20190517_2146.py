# Generated by Django 2.2.1 on 2019-05-17 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0004_auto_20190517_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='rent_amount',
            field=models.DecimalField(decimal_places=0, max_digits=4),
        ),
    ]
