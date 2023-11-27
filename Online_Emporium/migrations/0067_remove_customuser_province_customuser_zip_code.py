# Generated by Django 4.2.7 on 2023-11-25 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Online_Emporium', '0066_order_payment_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='province',
        ),
        migrations.AddField(
            model_name='customuser',
            name='zip_code',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]