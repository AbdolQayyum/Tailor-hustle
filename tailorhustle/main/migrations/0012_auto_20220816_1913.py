# Generated by Django 3.2.12 on 2022-08-16 19:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_post_date_posted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='post',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 16, 19, 13, 51, 349733)),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]