# Generated by Django 3.2.12 on 2022-05-28 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_postviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postviews',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
