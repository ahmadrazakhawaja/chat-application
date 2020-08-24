from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json
from itertools import chain

from .models import User,contacts,groups,groupcontact,groupadmin,groupcreator,notifications,usermessages
from .consumers import ChatConsumer2
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.

def index(request):
    lx=""
    dj=[]
    jb=[]
    lq=""
    if request.user.is_authenticated:
        lx = contacts.objects.filter(User_id=request.user.id)
        lq = groupcontact.objects.filter(members=request.user.id)
        for nb in lq:
            jb.append(groups.objects.get(id=nb.group_id))
        for kn in lx:
            dj.append(User.objects.get(username=kn.contact))

            

        
    return render(request, "chat/index.html",{
    "contacts":dj,
    "groups":jb
})

@login_required
def room(request, room_name):
    if request.user.is_authenticated:
        lx=""
        dj=[]
        jb=[]
        lq=""
        lx = contacts.objects.filter(User_id=request.user.id)
        lq = groupcontact.objects.filter(members=request.user.id)
        for nb in lq:
            jb.append(groups.objects.get(id=nb.group_id))
        for kn in lx:
            dj.append(User.objects.get(username=kn.contact))
        lx = contacts.objects.filter(User_id=request.user.id,channel=room_name)
        if not lx:
            pass
        else:
            vb = contacts.objects.filter(User_id=request.user.id,channel=room_name)[0].contact
            return render(request, 'chat/room.html', {
                'room_name': room_name,
                'contactname':vb,
                'contacts': dj,
                'groups':jb,
                'back':True

            })


        if not groups.objects.filter(group_name=room_name):
            return HttpResponseRedirect('/')
        else:
            if not groupcontact.objects.filter(group_id=groups.objects.get(group_name=room_name).id,members=request.user.id):
                return HttpResponseRedirect('/')
            else:
                edx=[]
                membersz=groupcontact.objects.filter(group_id=groups.objects.get(group_name=room_name).id)
                adminx=groupadmin.objects.filter(group_id=groups.objects.get(group_name=room_name).id)
                ado=False
                mnk = groupadmin.objects.filter(group_id=groups.objects.get(group_name=room_name).id,User_id=request.user.id)
                if not mnk:
                    ado=False
                else:
                    ado=True

                adminx
                jp=[]
                for lu in adminx:
                    jp.append(User.objects.get(id=lu.User_id))
                print(jp)
                check=False
                for xy in membersz:
                    check=False
                    for bn in adminx:
                        if bn.User_id==xy.members:
                            check=True
                            break
                    if check==False:
                        edx.append(User.objects.get(id=xy.members))


                return render(request, 'chat/group.html', {
                    'room_name': room_name,
                    'members':edx,
                    'admin':jp,
                    'back':True,
                    'adminv':ado

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
            return render(request, "chat/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "chat/login.html")

def logout_view(request):
    user= User.objects.get(id=request.user.id)
    user.status="Offline"
    username = user.username
    user.save()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("chat_", {"type": "chat_message",'username': username,'status': "Offine"})
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
            return render(request, "chat/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            if username=="":
                return render(request, "chat/register.html", {
                "message": "Username cannot be empty."
            })
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "chat/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chat/register.html")


def addcontact(request):
    if request.method=='POST':
        data = json.loads(request.body)
        ax = data.get('content')
        am=ax
        room_name=ax
        if not User.objects.filter(username=ax):
            return JsonResponse({
                    "message": "Username doesnot exist"
                }, status=400)
        vk = User.objects.get(username=ax).id
        vm = User.objects.get(id=request.user.id).username
        if contacts.objects.filter(User_id=request.user.id,contact=ax):
            return JsonResponse({
                    "message": "Contact already exists",
                }, status=201)
        if not contacts.objects.filter(channel=ax):
            contacts(User_id=request.user.id,contact=ax,channel=ax).save()
            contacts(User_id=vk,contact=vm,channel=ax).save()
        else:
            count=0
            while True:
                count=count+1
                ax=ax+"x"+f"{count}"
                if not contacts.objects.filter(channel=ax):
                    contacts(User_id=request.user.id,contact=am,channel=ax).save()
                    contacts(User_id=vk,contact=vm,channel=ax).save()
                    break
                ax=am

        ax=am
        jx = contacts.objects.filter(User_id=request.user.id)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("chat_", {"type": "newcontact",'room': f"{request.user.username}",'message':"contact",'id':f"{request.user.id}"})
        return JsonResponse({
                    "message": "Contact added",
                    "content": data.get('content'),
                    "status":User.objects.get(username=data.get('content')).status,
                    'room_namex':room_name
                },safe=False, status=201)

    else:
        return JsonResponse({
                    "message": "Wrong request method"
                }, status=400)

def contact(request,name):
    bv = contacts.objects.filter(User_id=request.user.id,contact=name)
    if not bv:
        ak = groups.objects.filter(group_name=name)
        if not ak:
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect(reverse('room',args=[f'{ak[0].group_name}']))
    else:
        return HttpResponseRedirect(reverse('room',args=[f'{bv[0].channel}']))


def addgroup(request):
    data = json.loads(request.body)
    ax = data.get('content')
    if len(ax)>19:
        return JsonResponse({
                    "message": "Group name has too many characters",
                }, status=400)
    if ax=='':
        return JsonResponse({
                    "message": "Group name cannot be empty.",
                }, status=400)
    if not groups.objects.filter(group_name=ax):
        sk = groups(group_name=ax)
        sk.save()
        jk = groupcontact(group_id=sk.id,members=request.user.id)
        jk.save()
        bhk = groupadmin(group_id=sk.id,User_id=request.user.id)
        bhk.save()
        bhm = groupcreator(group_id=sk.id,User_id=request.user.id)
        bhm.save()
        return JsonResponse({
                    "message": "Group created",
                    "group_name": data.get('content')
                }, status=201)
    else:
         return JsonResponse({
                    "message": "Group name taken please choose a new name.",
                }, status=400)

def addmember(request):
    data = json.loads(request.body)
    ax = data.get('content')
    bx= data.get('channel')
    if not User.objects.filter(username=ax):
        return JsonResponse({
                    "message": "Username doesnot exist",
                }, status=400)
    else:
        jm = groups.objects.get(group_name=bx[1:len(bx)-1]).id
        if not groupcontact.objects.filter(group_id=jm,members=User.objects.get(username=ax).id):
            groupcontact(group_id=jm,members=User.objects.get(username=ax).id).save()
        else:
            return JsonResponse({
                    "message": "User already added",
                }, status=201)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("chat_", {"type": "newcontact",'room': f"{bx[1:len(bx)-1]}",'message':"group",'id':f"{request.user.id}"})
        notifications(User_id=User.objects.get(username=ax).id,channel=bx[1:len(bx)-1],message=f"{ax} has been added to the Group").save()
        usermessages(sender_id=request.user.id,reciever=bx[1:len(bx)-1],content=f"{ax} has been added to the Group").save()
        async_to_sync(channel_layer.group_send)("chat_", {"type": "notify",'room': f"{ax}",'message':"group"})
        strs = bx[1:len(bx)-1]+"setting"
        strk = "chat_%s" % strs
        stm = "chat_%s" % bx[1:len(bx)-1]
        async_to_sync(channel_layer.group_send)(strk, {"type": "chat_message",'message': "add",'username':f"{ax}",'id':f"{request.user.id}"})
        async_to_sync(channel_layer.group_send)(stm, {"type": "chat_message",'message': f"{ax} has been added to the Group"})
        async_to_sync(channel_layer.group_send)(stm, {"type": "add",'message': f"{ax}"})
        return JsonResponse({
                    "message": "member added",
                    "member": User.objects.get(username=ax).username,
                    "status": User.objects.get(username=ax).status
                }, status=201)

def setting(request,name):
    lx=""
    dj=[]
    jb=[]
    lq=""
    creator=False
    if request.user.is_authenticated:
        if not groupadmin.objects.filter(User_id=request.user.id,group_id=groups.objects.get(group_name=name).id):
            return  HttpResponseRedirect('/')
        else:
            lx = contacts.objects.filter(User_id=request.user.id)
            dpo=[]
            mx = groupadmin.objects.filter(group_id=groups.objects.get(group_name=name).id)
            for cv in mx:
                dpo.append(User.objects.get(id=cv.User_id))
            la = User.objects.filter()
            lq = groupcontact.objects.filter(group_id=groups.objects.get(group_name=name).id)
            for nb in lq:
                jb.append(User.objects.get(id=nb.members))
            for kn in lx:
                dj.append(User.objects.get(username=kn.contact))
                creator=False
                if not groupcreator.objects.filter(group_id=groups.objects.get(group_name=name).id,User_id=request.user.id):
                    creator=True
                else:
                    creator=False

        return render(request, 'chat/setting.html', {
                    'room_name':name,
                    'id':request.user.id,
                    'contacts':lx,
                    'groupy':jb,
                    'admin':dpo,
                    'back':True,
                    'creator':creator
                })

def remove(request):
    data = json.loads(request.body)
    ax = data.get('content')
    bx= data.get('channel')
    if not User.objects.filter(username=ax):
        return JsonResponse({
                    "message": "Username doesnot exist",
                }, status=400)
    else:
        jm = groups.objects.get(group_name=bx[1:len(bx)-1]).id
        if not groupcontact(group_id=jm,members=User.objects.get(username=ax).id):
            return JsonResponse({
                    "message": "User already removed"
                }, status=201)
        else:
            groupcontact.objects.get(group_id=jm,members=User.objects.get(username=ax).id).delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("chat_", {"type": "newcontact",'room': f"{bx[1:len(bx)-1]}",'message':"remove",'id':f"{request.user.id}"})
        notifications(User_id=User.objects.get(username=ax).id,channel=bx[1:len(bx)-1],message=f"{ax} has been removed from the Group").save()
        usermessages(sender_id=request.user.id,reciever=bx[1:len(bx)-1],content=f"{ax} has been removed from the Group").save()
        async_to_sync(channel_layer.group_send)("chat_", {"type": "notify",'room': f"{ax}",'message':"group"})
        strs = bx[1:len(bx)-1]+"setting"
        strk = "chat_%s" % strs
        stm = "chat_%s" % bx[1:len(bx)-1]
        async_to_sync(channel_layer.group_send)(strk, {"type": "chat_message",'message': "remove",'username':f"{ax}",'id':f"{request.user.id}"})
        async_to_sync(channel_layer.group_send)(stm, {"type": "chat_message",'message': f"{ax} has been removed from the Group"})
        async_to_sync(channel_layer.group_send)(stm, {"type": "remove",'message': f"{ax}"})
        return JsonResponse({
                    "message": "member added",
                    "member": User.objects.get(username=ax).username,
                    "status": User.objects.get(username=ax).status
                }, status=201)

def addadmin(request):
    data = json.loads(request.body)
    ax = data.get('content')
    bx= data.get('channel')
    if not User.objects.filter(username=ax):
        return JsonResponse({
                    "message": "Username doesnot exist",
                }, status=400)
    else:
        jm = groups.objects.get(group_name=bx[1:len(bx)-1]).id
        if not groupcontact(group_id=jm,members=User.objects.get(username=ax).id):
            return JsonResponse({
                    "message": "User is not in the Group."
                }, status=201)
        else:
            if not groupadmin.objects.filter(group_id=jm,User_id=User.objects.get(username=ax).id):
                groupadmin(group_id=jm,User_id=User.objects.get(username=ax).id).save()
            else:
                return JsonResponse({
                    "message": "User is already admin."
                }, status=201)

        message = f"you have given admin rights to {ax}"
        notifications(User_id=User.objects.get(username=ax).id,channel=bx[1:len(bx)-1],message=f"{ax} has been given the admin rights").save()
        usermessages(sender_id=request.user.id,reciever=bx[1:len(bx)-1],content=f"{ax} has been given the admin rights").save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("chat_", {"type": "notify",'room': f"{ax}",'message':"group"})
        strs = bx[1:len(bx)-1]+"setting"
        strk = "chat_%s" % strs
        stm = "chat_%s" % bx[1:len(bx)-1]
        async_to_sync(channel_layer.group_send)(strk, {"type": "chat_message",'message': "add admin",'username':f"{ax}",'id':f"{request.user.id}"})
        async_to_sync(channel_layer.group_send)(stm, {"type": "chat_message",'message': f"{ax} has been given the admin rights"})
        async_to_sync(channel_layer.group_send)(stm, {"type": "addadmin",'message': f"{ax}"})
        return JsonResponse({
                    "message": message,
                    "member": User.objects.get(username=ax).username,
                    "status": User.objects.get(username=ax).status
                }, status=201)

def radmin(request):
    data = json.loads(request.body)
    ax = data.get('content')
    bx= data.get('channel')
    if not User.objects.filter(username=ax):
        return JsonResponse({
                    "message": "Username doesnot exist",
                }, status=400)
    else:
        jm = groups.objects.get(group_name=bx[1:len(bx)-1]).id
        if not groupcontact(group_id=jm,members=User.objects.get(username=ax).id):
            return JsonResponse({
                    "message": "User is not in the Group."
                }, status=400)
        else:
            if not groupadmin(group_id=jm,User_id=User.objects.get(username=ax).id):
                return JsonResponse({
                    "message": "User is not admin."
                }, status=400)
            else:
                if not groupcreator.objects.filter(group_id=jm,User_id=User.objects.get(username=ax).id):
                    groupadmin.objects.get(group_id=jm,User_id=User.objects.get(username=ax).id).delete()
                    notifications(User_id=User.objects.get(username=ax).id,channel=bx[1:len(bx)-1],message=f"{ax} has been removed from adminship").save()
                    usermessages(sender_id=request.user.id,reciever=bx[1:len(bx)-1],content=f"{ax} has been removed from adminship").save()
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)("chat_", {"type": "notify",'room': f"{ax}",'message':"group"})
                    strs = bx[1:len(bx)-1]+"setting"
                    strk = "chat_%s" % strs
                    stm = "chat_%s" % bx[1:len(bx)-1]
                    async_to_sync(channel_layer.group_send)(strk, {"type": "chat_message",'message': "remove admin",'username':f"{ax}",'id':f"{request.user.id}"})
                    async_to_sync(channel_layer.group_send)(stm, {"type": "chat_message",'message': f"{ax} has been removed from adminship"})
                    async_to_sync(channel_layer.group_send)(stm, {"type": "radmin",'message': f"{ax}"})
                    message = "you have been removed from adminship"
                    return JsonResponse({
                                "message": message,
                                "member": User.objects.get(username=ax).username,
                                "status": User.objects.get(username=ax).status
                            }, status=201)
                else:
                    return JsonResponse({
                                "message": 'Cant remove group creator from adminship',
                            }, status=400)


        notifications(User_id=User.objects.get(username=ax).id,channel=bx[1:len(bx)-1],message=f"{ax} has been removed from adminship").save()
        usermessages(sender_id=request.user.id,reciever=bx[1:len(bx)-1],content=f"{ax} has been removed from adminship").save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("chat_", {"type": "notify",'room': f"{ax}",'message':"group"})
        strs = bx[1:len(bx)-1]+"setting"
        strk = "chat_%s" % strs
        stm = "chat_%s" % bx[1:len(bx)-1]
        async_to_sync(channel_layer.group_send)(strk, {"type": "chat_message",'message': "remove admin",'username':f"{ax}",'id':f"{request.user.id}"})
        async_to_sync(channel_layer.group_send)(stm, {"type": "chat_message",'message': f"{ax} has been removed from adminship"})
        async_to_sync(channel_layer.group_send)(stm, {"type": "rsadmin",'message': f"{ax}"})
        message = "you have been removed from adminship"
        return JsonResponse({
                    "message": message,
                    "member": User.objects.get(username=ax).username,
                    "status": User.objects.get(username=ax).status
                }, status=201)


    








