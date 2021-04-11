# Generated by Django 3.1.2 on 2020-10-14 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0015_upload_post_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='context',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='attachment',
            name='converted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='attach',
            field=models.FileField(blank=True, upload_to='files'),
        ),
    ]
