# Generated by Django 2.2.1 on 2019-05-16 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rental', '0001_initial'),
        ('quittance', '0001_initial'),
        ('occupant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quittance',
            name='bedroom_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bedroom', to='rental.Bedroom', verbose_name='related bedroom'),
        ),
        migrations.AddField(
            model_name='quittance',
            name='occupant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='occupant', to='occupant.Occupant', verbose_name='related occupant'),
        ),
        migrations.AddField(
            model_name='quittance',
            name='property_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property', to='rental.Property', verbose_name='related property'),
        ),
    ]
