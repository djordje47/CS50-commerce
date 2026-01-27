from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Auction(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=700)
    bid = models.IntegerField()
    image = models.CharField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")

    def __str__(self):
        return f"{self.id} - {self.title} - {self.category.name}"


class WatchList(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.auction.title} - {self.user.username}"


class Bid(models.Model):
    auction = models.ManyToManyField(Auction, blank=False, related_name="bids")
    user = models.ManyToManyField(User, blank=False, related_name="bids")
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.id} - {self.bid}"


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return f"{self.auction.title} - {self.user.username} - {self.comment}"
