# Generated by Django 4.1.1 on 2022-11-21 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0005_alter_order_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='commerce.orderitem'),
        ),
    ]
