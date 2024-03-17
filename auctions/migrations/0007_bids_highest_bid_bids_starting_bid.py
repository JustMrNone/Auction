# Generated by Django 5.0.1 on 2024-03-15 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auction_listing_highest_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='highest_bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='bids',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
