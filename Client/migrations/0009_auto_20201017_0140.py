# Generated by Django 3.1.2 on 2020-10-16 20:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Client', '0008_admin_adminparent_adminstudent_adminteacher'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Admin',
            new_name='Administrator',
        ),
    ]