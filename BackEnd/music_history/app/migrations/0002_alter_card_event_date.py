# Generated by Django 4.2.5 on 2023-09-18 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='event_date',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
