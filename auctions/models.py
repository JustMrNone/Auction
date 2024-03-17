from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    name = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return f"User: {self.name} {self.lastname}"
    
class auction_listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    category = models.CharField(max_length=100, blank=True)
    image_url = models.ImageField(upload_to='auction_images/', blank=True, null=True )  # Define the ImageField
    bidss = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=100, blank=True, null=True)
    highest_bid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now=True)
    auction = models.ForeignKey(auction_listing, on_delete=models.CASCADE, related_name='bids')  # Add related_name
    highest_bid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    starting_bid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    
    def __str__(self):
        return f'{self.amount} on {self.auction} by {self.user.username}'

class auction_listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    category = models.CharField(max_length=100, blank=True)
    image_url = models.ImageField(upload_to='auction_images/', blank=True, null=True )  # Define the ImageField
    bidss = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=100, blank=True, null=True)
    highest_bid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now=True)
    auction = models.ForeignKey(auction_listing, on_delete=models.CASCADE, related_name='bids')  # Add related_name
    highest_bid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    starting_bid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    
    def __str__(self):
        return f'{self.amount} on {self.auction} by {self.user.username}'


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('auction_listing')

    def add_item(self, item):
        self.items.add(item)
        

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(auction_listing, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.listing.title} - {self.created_at}'
        
        