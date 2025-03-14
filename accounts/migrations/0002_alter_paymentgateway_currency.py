# Generated by Django 5.0.7 on 2025-03-12 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentgateway',
            name='currency',
            field=models.CharField(choices=[('BTC', 'Bitcoin'), ('USDT(TRC)', 'USDT(TRC)'), ('USDT(ETH)', 'USDT(ETH)'), ('ETH', 'Ethereum'), ('LTC', 'Litecoin'), ('TRX', 'Tron'), ('BCH', 'Bitcoin Cash')], max_length=10),
        ),
    ]
