# Generated by Django 5.0.1 on 2024-03-15 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_bids_auction_alter_user_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='image_url',
            field=models.ImageField(upload_to='auction_images/'),
        ),
    ]