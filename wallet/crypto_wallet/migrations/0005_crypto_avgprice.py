# Generated by Django 5.0.3 on 2024-03-09 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_wallet', '0004_delete_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='crypto',
            name='avgPrice',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
