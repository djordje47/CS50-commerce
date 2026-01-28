from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from auctions.models import Auction
from auctions.forms import AuctionForm


def index(request):
    listings = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def show_listing(request, listing_id):
    listing = Auction.objects.get(id=listing_id)
    watch_list = []
    if request.user.is_authenticated:
        watch_list = request.user.saved_listings.values_list('auction_id', flat=True)
    return render(request, 'auctions/listing.html', {
        "listing": listing,
        "bids": listing.bids.all().order_by("-bid"),
        "comments": listing.comments.all().order_by("-id"),
        "watch_list": watch_list,
    })


@login_required
def create_listing(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.owner = request.user
            new_listing.save()
            return HttpResponseRedirect(reverse("show_listing", args=[new_listing.id]))
        else:
            return render(request, 'auctions/create-listing.html', {'form': form})
    return render(request, 'auctions/create-listing.html', {
        "form": AuctionForm(),
    })


@login_required
def edit_listing(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)

    if request.method == "POST":
        form = AuctionForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("show_listing", args=[listing.id]))
        else:
            return render(request, 'auctions/edit-listing.html', {
                'form': form,
                'listing': listing,
            })
    return render(request, 'auctions/edit-listing.html', {
        "listing": listing,
        'form': AuctionForm(instance=listing),
    })
