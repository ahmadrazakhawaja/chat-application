from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class listing(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE,related_name="User")
    title = models.CharField(max_length=64)
    text = models.TextField()
    starting_bid = models.IntegerField()
    image_url = models.URLField()
    category = models.CharField(max_length=64)
    status = models.BooleanField()

    def __str__(self):
        return f"id:{self.id}:[ title: {self.title}, description:{self.text}, starting_bid:{self.starting_bid}, image_url:{self.image_url}, category:{self.category} ]"

class bid(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE,related_name="User1", null=True)
    listing = models.ForeignKey(listing,on_delete=models.CASCADE,related_name="listingb")
    highest_bid = models.IntegerField()

    def __str__(self):
        return f"id:{self.listing.id}: highest bid:{self.highest_bid}"



class comments(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE,related_name="User2")
    listing = models.ForeignKey(listing,on_delete=models.CASCADE,related_name="listingc")
    comments = models.TextField()

    def __str__(self):
        return f"id:{self.listing.id}: comment:{self.comments}"

class watchlist(models.Model):
    listing = models.ForeignKey(listing,on_delete=models.CASCADE,related_name="listinge")
    User = models.ForeignKey(User,on_delete=models.CASCADE,related_name="User3")

    def __str__(self):
        return f"id:{self.listing.id}: comment:{self.User.id}"


