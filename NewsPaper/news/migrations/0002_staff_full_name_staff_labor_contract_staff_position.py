# Generated by Django 4.2.6 on 2023-10-17 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='full_name',
            field=models.CharField(default=123, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='labor_contract',
            field=models.IntegerField(default=123),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='position',
            field=models.CharField(default=123, max_length=255),
            preserve_default=False,
        ),
    ]
