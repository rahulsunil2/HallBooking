# Generated by Django 2.2 on 2020-04-16 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hall', '0005_auto_20200416_1913'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='booking',
            name='fId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hall.Faculty'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='inCharge',
            field=models.ForeignKey(default=1234, on_delete=django.db.models.deletion.PROTECT, to='hall.Faculty'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
