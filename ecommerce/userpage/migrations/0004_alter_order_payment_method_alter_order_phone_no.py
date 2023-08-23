# Generated by Django 4.1.7 on 2023-06-13 20:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0003_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Cash on Delivery', 'Cash on Delivery'), ('Esewa', 'Esewa'), ('Khalti', 'Khalti')], max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone_no',
            field=models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(9), django.core.validators.MaxLengthValidator(20)]),
        ),
    ]