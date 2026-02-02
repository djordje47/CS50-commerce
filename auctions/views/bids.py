from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from auctions.forms import BidForm
from auctions.models import Auction


@login_required
def create_auction_bid(request, listing_id):
    user = request.user
    auction = Auction.objects.get(id=listing_id)

    if not auction.is_active:
        messages.error(request, "The listing is closed.", extra_tags='danger')
        return HttpResponseRedirect(reverse('index'))

    form = BidForm(request.POST)
    if form.is_valid():
        current_bid = form.cleaned_data['bid']
        highest_bid = auction.get_highest_bid_amount()
        if not current_bid > highest_bid:
            messages.error(request, f"You can't bid lower than the highest bid: {highest_bid}", extra_tags='danger')
            return HttpResponseRedirect(reverse('show_listing', args=[listing_id]))
        new_bid = form.save(commit=False)
        new_bid.auction = auction
        new_bid.user = user
        new_bid.save()
        messages.success(request, "Bid placed successfully!")
        return HttpResponseRedirect(reverse('show_listing', args=[listing_id]))
