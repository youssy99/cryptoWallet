# Generated by Django 5.0.3 on 2024-03-09 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_wallet', '0007_crypto_currencytype'),
    ]

    operations = [
        migrations.AddField(
            model_name='crypto',
            name='variation',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]