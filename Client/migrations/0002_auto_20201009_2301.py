# Generated by Django 3.1.2 on 2020-10-09 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Client', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Scores',
            new_name='Score',
        ),
    ]