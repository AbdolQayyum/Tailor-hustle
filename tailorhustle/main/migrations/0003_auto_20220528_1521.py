# Generated by Django 3.2.12 on 2022-05-28 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_post_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='pic',
            new_name='post_file',
        ),
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(default=None, max_length=255),
        ),
    ]