# Generated by Django 4.1.3 on 2022-11-15 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_product_sub_image2_product_sub_image3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=250),
        ),
    ]