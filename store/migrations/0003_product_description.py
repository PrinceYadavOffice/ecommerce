# Generated by Django 3.2.9 on 2021-11-17 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=400, null=True),
        ),
    ]
