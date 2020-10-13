# Generated by Django 3.1.2 on 2020-10-13 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0008_bannerconfig_bannerconfigentry'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bannerconfig',
            options={'verbose_name_plural': 'Banner config'},
        ),
        migrations.AlterModelOptions(
            name='bannerconfigentry',
            options={'verbose_name_plural': 'Banner config entries'},
        ),
        migrations.RemoveField(
            model_name='bannerconfigentry',
            name='value',
        ),
        migrations.AddField(
            model_name='bannerconfigentry',
            name='x1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bannerconfigentry',
            name='x2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bannerconfigentry',
            name='y1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bannerconfigentry',
            name='y2',
            field=models.IntegerField(default=0),
        ),
    ]