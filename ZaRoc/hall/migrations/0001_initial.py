# Generated by Django 2.1.5 on 2020-03-19 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('bId', models.DecimalField(decimal_places=0, max_digits=10, primary_key=True, serialize=False)),
                ('sTime', models.DateTimeField(verbose_name='Start Time')),
                ('eTime', models.DateTimeField(verbose_name='End Time')),
                ('eventName', models.CharField(max_length=60)),
                ('eventDetails', models.TextField(blank=True, verbose_name='Event Details')),
            ],
            options={
                'verbose_name_plural': 'Bookings',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.DecimalField(decimal_places=0, max_digits=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('dept', models.CharField(max_length=60)),
                ('auth_level', models.DecimalField(decimal_places=0, max_digits=1)),
            ],
            options={
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=4, unique=True)),
                ('name', models.CharField(max_length=60)),
                ('capacity', models.DecimalField(decimal_places=0, max_digits=3)),
                ('inCharge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hall.Faculty')),
            ],
            options={
                'verbose_name_plural': 'Halls',
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='fId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hall.Faculty'),
        ),
        migrations.AddField(
            model_name='booking',
            name='hallNo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hall.Hall'),
        ),
    ]
