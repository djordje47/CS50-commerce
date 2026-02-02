from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('saved-listings', views.saved_listings, name='saved_listings'),
    path('my-listings', views.my_listings, name='my_listings'),
    path("create-listing", views.create_listing, name="create_listing"),
    path("edit-listing/<int:listing_id>", views.edit_listing, name="edit_listing"),
    path("watch-listing/<int:listing_id>", views.watch_listing, name="watch_listing"),
    path("unwatch-listing/<int:listing_id>", views.unwatch_listing, name="unwatch_listing"),
    path("listing/<int:listing_id>", views.show_listing, name='show_listing'),
    path("close-listing/<int:listing_id>", views.close_listing, name='close_listing'),
    path('add-comment/<int:listing_id>', views.add_comment, name='add_comment'),
    path('categories', views.all_categories, name='all_categories'),
    path('categories/<int:category_id>', views.category_listings, name='category_listings'),
    path('create-auction-bid/<int:listing_id>', views.create_auction_bid, name='create_auction_bid'),
]
