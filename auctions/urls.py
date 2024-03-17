from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path('create/', views.create_listing, name='create_listing'),
    path('accounts/login/', views.login_view, name='login'),
    path('add_to_watchlist/<int:item_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:item_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('add_comment/<int:listing_id>/', views.add_comment, name='add_comment'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('category/<str:category>/', views.category_page, name='category_page'),
    path("filter", views.filter, name="filter"),
    path('update_bid/<int:id>/', views.update_bid, name='update_bid'),
    path('bids/', views.bidss, name='bids'),
    path('close_bids/<int:auction_id>/', views.close_bids, name='close_bids'),
    path('close_bids/<int:id>/', views.close_bids, name='close_bids'),
    path('categories/<str:category>/', views.category_listings, name='category_listings'),
    path('delete_bid/<int:bid_id>/', views.delete_bid, name='delete_bid'),
    
]