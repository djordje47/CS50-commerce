from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, WatchList
from .forms import AuctionForm


def index(request):
    listings = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def show_listing(request, listing_id):
    listing = Auction.objects.get(id=listing_id)
    watch_list = request.user.saved_listings.values_list('auction_id', flat=True)
    return render(request, 'auctions/listing.html', {
        "listing": listing,
        "bids": listing.bids.all().order_by("-bid"),
        "comments": listing.comments.all().order_by("-id"),
        "watch_list": watch_list,
    })


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


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
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
