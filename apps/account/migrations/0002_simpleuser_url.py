# Generated by Django 4.1.7 on 2023-03-11 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='simpleuser',
            name='url',
            field=models.URLField(default='abc'),
            preserve_default=False,
        ),
    ]
