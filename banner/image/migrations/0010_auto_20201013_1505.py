# Generated by Django 3.1.2 on 2020-10-13 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0009_auto_20201013_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerconfigentry',
            name='x1',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='bannerconfigentry',
            name='x2',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='bannerconfigentry',
            name='y1',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='bannerconfigentry',
            name='y2',
            field=models.IntegerField(default=-1),
        ),
    ]
