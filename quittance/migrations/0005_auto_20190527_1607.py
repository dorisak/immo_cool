# Generated by Django 2.2.1 on 2019-05-27 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quittance', '0004_quittance_rental'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quittance',
            name='date_of_payment',
            field=models.DateField(blank=True),
        ),
    ]
