# Generated by Django 5.0.1 on 2024-03-15 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.auction_listing'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.DeleteModel(
            name='AuctionListing',
        ),
    ]
