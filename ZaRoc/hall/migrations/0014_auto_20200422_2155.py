# Generated by Django 2.2.1 on 2020-04-22 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hall', '0013_auto_20200422_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='edate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='etime',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='sdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='stime',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
