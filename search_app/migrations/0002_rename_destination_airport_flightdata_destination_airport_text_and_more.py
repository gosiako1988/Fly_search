# Generated by Django 4.2.7 on 2023-12-04 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flightdata',
            old_name='destination_airport',
            new_name='destination_airport_text',
        ),
        migrations.RenameField(
            model_name='flightdata',
            old_name='destination_city',
            new_name='fly_from',
        ),
        migrations.RenameField(
            model_name='flightdata',
            old_name='origin_airport',
            new_name='fly_to',
        ),
        migrations.RenameField(
            model_name='flightdata',
            old_name='origin_city',
            new_name='origin_airport_text',
        ),
        migrations.RenameField(
            model_name='flightdata',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RemoveField(
            model_name='flightdata',
            name='out_date',
        ),
        migrations.RemoveField(
            model_name='flightdata',
            name='return_date',
        ),
        migrations.RemoveField(
            model_name='flightdata',
            name='stop_overs',
        ),
        migrations.RemoveField(
            model_name='flightdata',
            name='via_city',
        ),
        migrations.AddField(
            model_name='flightdata',
            name='adults',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='flightdata',
            name='children',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='flightdata',
            name='date_from',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='flightdata',
            name='date_to',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='flightdata',
            name='infants',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='flightdata',
            name='return_from',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='flightdata',
            name='return_to',
            field=models.DateField(null=True),
        ),
    ]
