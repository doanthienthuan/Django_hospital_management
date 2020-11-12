# Generated by Django 3.1.1 on 2020-10-11 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phongkham', '0005_patient_bhyt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctor',
            options={'ordering': ['id', 'first_name', 'last_name']},
        ),
        migrations.AlterModelOptions(
            name='manager',
            options={'ordering': ['id', 'first_name', 'last_name']},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'ordering': ['id', 'first_name', 'last_name']},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'ordering': ['id', 'first_name', 'last_name']},
        ),
        migrations.AddField(
            model_name='medicalrecord',
            name='medicine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='phongkham.medicine'),
        ),
    ]