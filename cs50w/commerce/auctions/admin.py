from django.contrib import admin

from .models import User, listing, bid, comments, watchlist
# Register your models here.
admin.site.register(listing)
admin.site.register(bid)
admin.site.register(comments)