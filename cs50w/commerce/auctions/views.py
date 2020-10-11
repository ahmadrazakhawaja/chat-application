from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import string

from .models import User, listing, bid, comments, watchlist


def index(request):
    return render(request, "auctions/index.html",{
        "listings":listing.objects.filter(status=True) ,
        "bid":bid.objects.all()

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

@login_required
def create(request):
    if request.method =='POST':
        title = request.POST['title']
        text = request.POST['description']
        bidl = request.POST['bid']
        url = request.POST['url']
        category = request.POST['category']
        m = listing(User_id=f"{request.user.id}",title=f"{title}",text=f"{text}",starting_bid=f"{bidl}",image_url=f"{url}",category=f"{category}",status=True)
        m.save()
        s = bid(listing_id=f"{m.id}", highest_bid=f"{bidl}")
        s.save()
        return HttpResponseRedirect(reverse("index"))
        


        
    else:
        return render(request, "auctions/create.html")


def listingc(request,id):
    if request.method == 'POST':
        if 'closem' in request.POST:
            lk = listing.objects.get(id=f"{id}")
            lk.status = False
            lk.save()
            return HttpResponseRedirect(reverse('listing',args=[f'{id}']))
        
        elif 'removew' in request.POST:
            lk = watchlist.objects.get(listing_id=f"{id}",User_id=f"{request.user.id}")
            lk.delete()
            return HttpResponseRedirect(reverse('listing',args=[f'{id}']))

        elif 'w' in request.POST:
            lk = watchlist(listing_id=f"{id}",User_id=f"{request.user.id}")
            lk.save()
            return HttpResponseRedirect(reverse('listing',args=[f'{id}']))

        elif 'bidsubmit' in request.POST:
            lk = bid.objects.get(listing_id=f"{id}")
            sk = listing.objects.get(id=f"{id}")
            ek=True
            if request.user.id!=None:
                if not watchlist.objects.filter(listing_id=f"{id}",User_id=f"{request.user.id}"):
                    ek=False
                else:
                    ek=True
            
            nk = comments.objects.filter(listing_id=f"{id}")
            mk=[]
            add = True
            for luk in nk:
                add = True
                for jk in mk:
                    if User.objects.get(id=luk.User_id)==jk:
                        add = False
                        break
                if add == True:
                    mk.append(User.objects.get(id=luk.User_id))

            message = ""
            if listing.objects.get(id=f"{id}").status == False:
                if request.user.id == bid.objects.get(listing_id=f"{id}").User_id:
                    message = "Congratulations you won This Item."
            if lk.User_id==None:
                if int(request.POST["bidamount"])<sk.starting_bid:
                    return render(request, "auctions/listing.html", {
                        "Message": message,
                        "Error": "Bid Amount should be larger than or equal to starting bid.",
                        "listings": sk,
                        "bid": bid.objects.get(listing_id=f"{id}"),
                        "comments": comments.objects.filter(listing_id=f"{id}"),
                        "watchlist": ek,
                        "high_bid": int(bid.objects.get(listing_id=f"{id}").highest_bid)+1,
                        "users": mk
                    })
                else:
                    lk.highest_bid = int(request.POST["bidamount"])
                    lk.User_id = int(request.user.id)
                    lk.save()
                    return HttpResponseRedirect(reverse('listing',args=[f'{id}']))
            else:
                if int(request.POST["bidamount"])<=lk.highest_bid:
                    return render(request, "auctions/listing.html", {
                         "Message": message,
                        "Error": "Bid Amount should be larger than Highest Bid.",
                        "listings": sk,
                        "bid": bid.objects.get(listing_id=f"{id}"),
                        "comments": comments.objects.filter(listing_id=f"{id}"),
                        "watchlist": ek,
                        "high_bid": int(bid.objects.get(listing_id=f"{id}").highest_bid)+1,
                        "users": mk
                    })

                else:
                    lk.highest_bid = int(request.POST["bidamount"])
                    lk.User_id = int(request.user.id)
                    lk.save()
                    return HttpResponseRedirect(reverse('listing',args=[f'{id}']))
    
        else:
            if 'addcomment' in request.POST:
                ek=True
                if request.user.id!=None:
                    if not watchlist.objects.filter(listing_id=f"{id}",User_id=f"{request.user.id}"):
                        ek=False
                    else:
                        ek=True
                com = comments(User_id=f"{request.user.id}",listing_id=f"{id}")
                com.comments = request.POST['comment']
                com.save()
                return HttpResponseRedirect(reverse('listing',args=[f'{id}']))

                    

                    
    else:
        ek=True
        if request.user.id!=None:
            if not watchlist.objects.filter(listing_id=f"{id}",User_id=f"{request.user.id}"):
                ek=False
            else:
                ek=True
        nk = comments.objects.filter(listing_id=f"{id}")
        mk=[]
        add = True
        for luk in nk:
            add = True
            for jk in mk:
                if User.objects.get(id=luk.User_id)==jk:
                    add = False
                    break
            if add == True:
                mk.append(User.objects.get(id=luk.User_id))

        message = ""
        if listing.objects.get(id=f"{id}").status == False:
            if request.user.id == bid.objects.get(listing_id=f"{id}").User_id:
                message = "Congratulations you won This Item."
            



        
        return render(request, "auctions/listing.html", {
                "Message": message,
                "listings": listing.objects.get(id=f"{id}"),
                "bid": bid.objects.get(listing_id=f"{id}"),
                "comments": comments.objects.filter(listing_id=f"{id}"),
                "watchlist": ek,
                "high_bid": int(bid.objects.get(listing_id=f"{id}").highest_bid)+1,
                "users": mk
            })

@login_required
def watchlistk(request):

    k = watchlist.objects.filter(User_id=f"{request.user.id}")
    lol=[]
    mk = []
    for sk in k:
        lol.append(listing.objects.get(id=f"{sk.listing_id}"))
        mk.append(bid.objects.get(listing_id=f"{sk.listing_id}"))

    return render(request, "auctions/watchlist.html",{
        "listings":lol ,
        "bid":mk

    })


def categoryl(request):

    k = listing.objects.filter(status=True)
    mk=[]
    equal = False
    for j in k:
        equal = False
        for n in mk:
            if j.category.upper() == n.upper():
                equal = True
                break
        if equal == False:
            mk.append(j.category)

    return render(request, "auctions/category.html",{
        "categories":mk 
    })


def categorylx(request,category):
    
    k = listing.objects.filter(category=f"{category}",status=True)
    mk = []
    for sk in k:
        mk.append(bid.objects.get(listing_id=f"{sk.id}"))
    return render(request, "auctions/category2.html",{
        "listings":k ,
        "bid":mk

    })


    
        


    

    

    



