# Generated by Django 3.1.1 on 2020-09-27 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phongkham', '0003_auto_20200603_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
