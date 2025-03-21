# Generated by Django 5.0.7 on 2025-03-12 12:23

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ForexPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('percentage', models.IntegerField(choices=[(5, '5%'), (69, '69%'), (120, '120%'), (200, '200%')])),
                ('duration', models.CharField(choices=[('After 6 Hours', 'After 6 Hours'), ('Hourly', 'Hourly'), ('Daily', 'Daily'), ('For 8 Hours', 'For 8 Hours'), ('Weekly', 'Weekly'), ('After 3 Months', 'After 3 Months'), ('After 6 Months', 'After 6 Months'), ('Forever', 'Forever')], max_length=20)),
                ('min_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentGateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_address', models.CharField(max_length=255, unique=True)),
                ('currency', models.CharField(choices=[('BTC', 'Bitcoin'), ('USDT(TRC)', 'USDT(TRC)'), ('USDT(ETH)', 'USDT(ETH)')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='email')),
                ('username', models.CharField(editable=False, max_length=100, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('fullname', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=15)),
                ('country', models.CharField(max_length=50)),
                ('profile_picture', models.ImageField(blank=True, default='profile_pics/profile_pic.webp', null=True, upload_to='profile_pics/')),
                ('groups', models.ManyToManyField(blank=True, related_name='accounts', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='accounts', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usdt_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('total_profits', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DepositTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniqid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('method', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('tx_ref', models.CharField(max_length=100, unique=True)),
                ('screenshot', models.ImageField(blank=True, null=True, upload_to='deposit_screenshots/')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('referral_code', models.CharField(max_length=10, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='referral', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionCodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('withdraw_code', models.CharField(blank=True, max_length=6, null=True)),
                ('withdraw_code_created_at', models.DateTimeField(auto_now=True)),
                ('withdraw_code_status', models.CharField(choices=[('active', 'Active'), ('used', 'Used'), ('expired', 'Expired')], default='active', max_length=10)),
                ('reset_code', models.CharField(blank=True, max_length=6, null=True)),
                ('reset_code_created_at', models.DateTimeField(auto_now=True)),
                ('reset_code_status', models.CharField(choices=[('active', 'Active'), ('used', 'Used'), ('expired', 'Expired')], default='active', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Users_Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniq_id', models.CharField(max_length=50, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('profit', models.DecimalField(decimal_places=2, max_digits=15)),
                ('daily_income', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total', models.DecimalField(decimal_places=2, max_digits=15)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='active', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WalletAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, unique=True)),
                ('currency', models.CharField(choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('USDT(TRC)', 'USDT(TRC)'), ('USDT(ETH)', 'USDT(ETH)'), ('LTC', 'Litecoin'), ('TRX', 'Tron'), ('BCH', 'Bitcoin Cash')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallet_addresses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WithdrawTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniqid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('currency', models.CharField(choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('USDT(TRC)', 'USDT(TRC)'), ('USDT(ETH)', 'USDT(ETH)'), ('LTC', 'Litecoin'), ('TRX', 'Tron'), ('BCH', 'Bitcoin Cash')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=7, max_digits=15)),
                ('withdraw_address', models.CharField(max_length=255, null=True)),
                ('tx_ref', models.CharField(max_length=100, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
