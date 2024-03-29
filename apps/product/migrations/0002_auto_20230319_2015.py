# Generated by Django 3.2.18 on 2023-03-19 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=223, null=True)),
                ('image', models.ImageField(null=True, upload_to='sales')),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.AddField(
            model_name='color',
            name='title',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productimage',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='product.color'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='banner_discount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.bannerdiscount'),
        ),
    ]
