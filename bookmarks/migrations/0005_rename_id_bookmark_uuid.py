# Generated by Django 4.2.3 on 2023-07-06 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0004_alter_bookmark_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmark',
            old_name='id',
            new_name='uuid',
        ),
    ]
