# Generated by Django 3.2.18 on 2023-04-06 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_productimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerdiscount',
            name='title',
            field=models.TextField(max_length=223, null=True),
        ),
    ]
