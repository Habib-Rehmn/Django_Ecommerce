# Generated by Django 4.2.4 on 2023-10-28 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Online_Emporium', '0062_remove_order_ordered_quantity_order_ordered_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ordered_quantity',
        ),
    ]