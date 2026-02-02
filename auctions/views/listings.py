from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from auctions.models import Auction
from auctions.forms import AuctionForm, BidForm, CommentForm


def index(request):
    listings = Auction.objects.filter(is_active=True).all()
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def my_listings(request):
    listings = request.user.listings.all()
    return render(request, "auctions/my-listings.html", {
        "listings": listings,
    })


def show_listing(request, listing_id):
    listing = Auction.objects.get(id=listing_id)
    watch_list = []
    bid_form = False
    comment_form = False
    if request.user.is_authenticated:
        watch_list = request.user.saved_listings.values_list('auction_id', flat=True)
        bid_form = BidForm()
        comment_form = CommentForm()
    print(listing.comments.all())
    return render(request, 'auctions/listing.html', {
        "listing": listing,
        "bids": listing.bids.all().order_by("-bid"),
        "comments": listing.comments.all().order_by("-id"),
        "watch_list": watch_list,
        "bid_form": bid_form,
        "comment_form": comment_form,
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


@login_required
def close_listing(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    if listing.owner.id == request.user.id:
        listing.is_active = False
        listing.winner = listing.get_auction_winner()
        listing.save()
        return HttpResponseRedirect(reverse("show_listing", args=[listing.id]))
    else:
        messages.error(request, "You are not the owner of this listing.", extra_tags="danger")
        return HttpResponseRedirect(reverse("index"))


@login_required
def add_comment(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.auction = listing
            comment.save()
            messages.success(request, "Your comment has been saved.")
        else:
            messages.error(request, 'Something went wrong.', extra_tags="danger")
        return HttpResponseRedirect(reverse('show_listing', args=[listing.id]))
    else:
        return HttpResponseRedirect(reverse('show_listing', args=[listing.id]))
