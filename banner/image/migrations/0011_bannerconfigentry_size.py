# Generated by Django 3.1.2 on 2020-10-13 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0010_auto_20201013_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannerconfigentry',
            name='size',
            field=models.IntegerField(default=-1),
        ),
    ]