# Generated by Django 3.1.2 on 2020-10-13 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0011_bannerconfigentry_size'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['points', 'name']},
        ),
    ]
