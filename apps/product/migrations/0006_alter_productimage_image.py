# Generated by Django 3.2.18 on 2023-03-25 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20230324_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(default='null', upload_to='products'),
            preserve_default=False,
        ),
    ]
