# Generated by Django 5.0.3 on 2024-03-09 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_wallet', '0006_crypto_actualprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='crypto',
            name='currencyType',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
