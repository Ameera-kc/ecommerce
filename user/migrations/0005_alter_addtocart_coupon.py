# Generated by Django 4.1.3 on 2022-11-22 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_addtocart_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addtocart',
            name='coupon',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='user.coupon'),
        ),
    ]
