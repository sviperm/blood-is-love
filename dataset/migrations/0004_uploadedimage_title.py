# Generated by Django 2.1.7 on 2019-04-15 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0003_auto_20190415_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedimage',
            name='title',
            field=models.TextField(default='default'),
            preserve_default=False,
        ),
    ]
