# Generated by Django 4.0.4 on 2022-12-03 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onestop', '0014_alter_cart_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='image',
            field=models.ImageField(default='', upload_to='product_images'),
        ),
    ]