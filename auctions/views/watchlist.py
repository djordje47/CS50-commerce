from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from auctions.models import Auction, User, WatchList

@login_required
def watch_listing(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    watch_list = WatchList(auction=listing, user=request.user)
    watch_list.save()
    messages.success(request, "Listing added to watchlist successfully!")
    return HttpResponseRedirect(reverse("show_listing", args=[listing_id]))


@login_required
def unwatch_listing(request, listing_id):
    watch_list_item = WatchList.objects.filter(auction=listing_id, user=request.user)
    watch_list_item.delete()
    messages.success(request, "Listing removed from watchlist successfully!")
    return HttpResponseRedirect(reverse("show_listing", args=[listing_id]))


@login_required
def saved_listings(request):
    user = User.objects.get(pk=request.user.id)
    user_saved_listings = WatchList.objects.filter(user=user).all().order_by("-id")
    return render(request, "auctions/saved-listings.html", {
        "saved_listings": user_saved_listings,
    })
