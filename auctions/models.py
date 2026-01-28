from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Auction(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=700)
    is_active = models.BooleanField(default=True)
    bid = models.IntegerField()
    image_url = models.URLField(default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name="listings")

    def __str__(self):
        return f"{self.id} - {self.title} - {self.category.name}"

    def get_highest_bid(self):
        highest_bid = self.bids.aggregate(models.Max('bid'))
        return highest_bid['bid__max']


class WatchList(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_listings")

    def __str__(self):
        return f"User: {self.user.username.capitalize()} watches {self.auction.title}"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, default=None, blank=False, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, default=None, blank=False, on_delete=models.CASCADE, related_name="bidders")
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.user.username.capitalize()} bids {self.bid} on {self.auction.title}"


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return f"Comment: {self.comment} by {self.user.username.capitalize()}"
