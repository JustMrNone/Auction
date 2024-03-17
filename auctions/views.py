from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .forms import ListingForm
from .models import User, auction_listing, Watchlist, Comment, bids
from django.contrib.auth.decorators import login_required
from django. contrib import messages
from django.db.models import Max
def index(request):
    listings = auction_listing.objects.all()# Fetch all listings
    bidss = bids.objects.all()# Fetch all bids
    context = {'listings': listings, 'bids':bidss }  # Use plural variable name
    return render(request, 'auctions/index.html', context)

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next") or reverse("index")
            return HttpResponseRedirect(next_url)
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


#this part was written by the studet 


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES) 
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {'form': form})


@login_required
def categories(request): 
    return render(request, "auctions/category.html")



@login_required
def add_to_watchlist(request, item_id):
    if request.method == 'POST':
        item = auction_listing.objects.get(pk=item_id)
        watchlist, created = Watchlist.objects.get_or_create(user=request.user)
        watchlist.items.add(item)
        return HttpResponseRedirect(reverse('watchlist'))  
    else:
        return HttpResponseRedirect(reverse('index'))
    
    

@login_required
def watchlist(request):
    watchlist = Watchlist.objects.get_or_create(user=request.user)[0]
    items = watchlist.items.all()
    return render(request, 'auctions/watchlist.html', {'items': items})



@login_required
def remove_from_watchlist(request, item_id):
    if request.method == 'POST':
        item = auction_listing.objects.get(pk=item_id)
        watchlist = Watchlist.objects.get_or_create(user=request.user)[0]
        watchlist.items.remove(item)
        return HttpResponseRedirect(reverse('watchlist'))  
    else:
        return HttpResponseRedirect(reverse('watchlist'))  
    
    
    
@login_required
def add_comment(request, listing_id):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        comment = Comment.objects.create(user=request.user, text=comment_text, listing_id=listing_id)
        return redirect('listing_detail', listing_id=listing_id)  
    else:
        return redirect('listing_detail', listing_id=listing_id)  
    
    
@login_required    
def listing_detail(request, listing_id):
    listing = get_object_or_404(auction_listing, pk=listing_id)
    
    user_auctions = auction_listing.objects.filter(user=request.user)
    user_bids = bids.objects.filter(auction__in=user_auctions)
    
    auction_bids = bids.objects.filter(auction=listing)
    

    highest_bid = auction_bids.aggregate(Max('amount'))['amount__max']
    highest_bidder = None
    if highest_bid is not None:
        highest_bid_obj = bids.objects.filter(auction=listing, amount=highest_bid).first()
        highest_bidder = highest_bid_obj.user
    
    
    user_bid = None
    if request.user.is_authenticated:
        user_bid = auction_bids.filter(user=request.user).first()
    

    winning_status = None
    if listing.is_closed and highest_bidder == request.user:
        winning_status = "Congratulations! You have won this auction."
    elif listing.is_closed:
        winning_status = "Sorry, you did not win this auction."
    
    context = {
        'listing': listing,
        'listing_comments': listing.comments.all(),
        'highest_bidder': highest_bidder,
        'user_bid': user_bid,
        'user_bids': user_bids,  
        'winning_status': winning_status,  
    }

    return render(request, 'auctions/listing_detail.html', context)



def category_page(request, category):
    listings = auction_listing.objects.filter(category__name__exact=category)
    context = {'listings': listings, 'category': category}
    return render(request, 'auctions/category.html', context)




@login_required
def filter(request):
    category_name = request.GET.get('category', '').strip().lower()
    title_query = request.GET.get('title', '').strip()  

    listings = auction_listing.objects.all()

    if category_name:
        listings = listings.filter(category__icontains=category_name)

    if title_query:
        listings = listings.filter(title__icontains=title_query)

    return render(request, 'auctions/category.html', {'listings': listings, 'category': category_name})


@login_required
def update_bid(request, id):
    try:
        auction = get_object_or_404(auction_listing, id=id)
        user_auctions = auction_listing.objects.filter(user=request.user)
        user_bids = bids.objects.filter(auction__in=user_auctions)
        auction_bids = bids.objects.filter(auction=auction)
        highest_bid = auction_bids.aggregate(Max('amount'))['amount__max']
        
        highest_bidder = None
        if highest_bid is not None:
            highest_bid_obj = bids.objects.filter(auction=auction, amount=highest_bid).first()
            highest_bidder = highest_bid_obj.user
        
        user_bid = None
        if request.user.is_authenticated:
            user_bid = auction_bids.filter(user=request.user).first()
        
        #print("Highest Bidder:", highest_bidder)  # Debugging statement
        #print("User Bid:", user_bid)              # Debugging statement

        if request.method == 'POST':
            amount = request.POST.get('bid')
            if amount:
                amount = float(amount)
                current_bid = auction.price if auction.price is not None else 0.0
                if amount > current_bid:
                    bid_obj, created = bids.objects.get_or_create(auction=auction, user=request.user)
                    bid_obj.amount = amount
                    bid_obj.save()
                    auction.price = amount
                    auction.save()
                    messages.success(request, 'Bid placed successfully!')
                    return HttpResponseRedirect(reverse('listing_detail', args=[id]))  
                else:
                    messages.error(request, 'Bid must be greater than the current bid value')
                    return HttpResponseRedirect(reverse('listing_detail', args=[id]))  
            else:
                messages.error(request, 'Invalid bid amount')
                return HttpResponseRedirect(reverse('listing_detail', args=[id]))  
    except Exception as e:
        print(e)
        messages.error(request, 'Invalid bid amount')
        return HttpResponseRedirect(reverse('listing_detail', args=[id]))
@login_required(login_url='auctions/login.html')
def bidss(request):
    user_auctions = auction_listing.objects.filter(user=request.user)
    
    user_bids = bids.objects.filter(auction__in=user_auctions)

    highest_bidders = {}
    for auction in user_auctions:
        highest_bid = bids.objects.filter(auction=auction).order_by('-amount').first()
        highest_bidders[auction.id] = highest_bid.user.username if highest_bid else None

    return render(request, 'auctions/bids.html', {'user_bids': user_bids, 'auctions': user_auctions, 'highest_bidders': highest_bidders})


@login_required(login_url='auctions/login.html')
def close_bids(request, auction_id):
    auction = get_object_or_404(auction_listing, id=auction_id)
    
    auction_bids = bids.objects.filter(auction=auction)
    if auction_bids.exists():
        highest_bid = auction_bids.order_by('-amount').first()
        
        auction.highest_bidder = highest_bid.user
        auction.save()
        
        if auction.image_url:
            auction.image_url.delete(save=False)
        auction.delete()
        
        messages.success(request, f"Bidding closed successfully. Highest Bidder: {highest_bid.user.username}")
    else:
        messages.warning(request, "No bids placed for this auction.")
    
    return redirect('index')




def category_listings(request, category):
    listings = auction_listing.objects.filter(category=category)
    context = {'listings': listings, 'category': category}
    return render(request, 'auctions/category_listings.html', context)

def delete_bid(request, bid_id):
    bid = get_object_or_404(bids, id=bid_id)
    auction_id = bid.auction.id
    bid.delete()
    return redirect('listing_detail', auction_id)
