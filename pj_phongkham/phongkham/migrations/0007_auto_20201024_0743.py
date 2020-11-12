# Generated by Django 3.1.1 on 2020-10-24 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phongkham', '0006_auto_20201011_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='room',
        ),
        migrations.RemoveField(
            model_name='medicalrecord',
            name='medicine',
        ),
        migrations.AddField(
            model_name='appointment',
            name='booked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]