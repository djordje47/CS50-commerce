from django.shortcuts import render
from auctions.models import Category


def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {
        'categories': categories
    })


def category_listings(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = category.listings.all()
    return render(request, 'auctions/category-listings.html', {
        'listings': listings,
        'category': category
    })
