# Generated by Django 2.2.1 on 2020-04-22 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hall', '0010_delete_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='eTime',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='sTime',
        ),
        migrations.AddField(
            model_name='booking',
            name='edate',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='etime',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='sdate',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='stime',
            field=models.TimeField(auto_now=True),
        ),
    ]
