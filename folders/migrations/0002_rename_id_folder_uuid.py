# Generated by Django 4.2.3 on 2023-07-06 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='folder',
            old_name='id',
            new_name='uuid',
        ),
    ]