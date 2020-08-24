# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from channels.db import database_sync_to_async
from .models import usermessages,User,groupcontact,groups,notifications,contacts



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        if self.scope['user'].is_anonymous:
            await self.close()
        
        else:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

        await self.accept()
        await self.write_status(self.scope['url_route']['kwargs']['room_name'],True)
        messages =  await self.get_messages(self.scope['url_route']['kwargs']['room_name'])
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': messages
            }
        )

        await self.remove_notification(self.room_group_name)

        


        
        


    async def disconnect(self, close_code):
        # Leave room group
        await self.write_status(self.scope['url_route']['kwargs']['room_name'],False)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        user = self.scope["user"]
        if text_data_json['group']=='contact':
            await self.write_message(user.id,message,self.scope['url_route']['kwargs']['room_name'],"contact")
        else:
            await self.write_message(user.id,message,self.scope['url_route']['kwargs']['room_name'],"group")


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': message
        }))

        await self.remove_notification(self.room_name)

    async def add(self, event):
        message = event['message']


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': message
        }))

    async def remove(self, event):
        message = event['message']


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': message
        }))
    
    async def addadmin(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': message
        }))

    async def radmin(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': message
        }))

    @database_sync_to_async
    def write_message(self,sender_id,message,room,contac):
        usermessages(sender_id=sender_id,reciever=room,content=message).save()
        if contac=='contact':
            nc = contacts.objects.get(User_id=self.scope['user'].id,channel=room).contact
            jpg = User.objects.get(username=nc).id
            notifications(User_id=jpg,channel=room,message="").save()
        else:
            mk = groupcontact.objects.filter(group_id=groups.objects.get(group_name=room).id)
            for lk in mk:
                notifications(User_id=lk.members,channel=room,message="").save()
    
    @database_sync_to_async
    def remove_notification(self,room):
        notifications.objects.filter(User_id=self.scope['user'].id,channel=room).delete()

    @database_sync_to_async
    def get_messages(self,room):
        messages = usermessages.objects.filter(reciever=room)
        ak=[]
        for message in messages:
            ak.append(message.content)
        return ak

    @database_sync_to_async
    def write_status(self,room,stat):
        user= User.objects.get(id=self.scope['user'].id)
        if stat == True: 
            user.status="Online"
        else:
            user.status="Offline"
        user.save()



class ChatConsumerx(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_x'
        if self.scope['user'].is_anonymous:
            await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
            return
        
        else:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

        await self.accept()
        noti=None
        if not self.scope['user'].is_anonymous:
            noti = await self.get_notify()

        if not self.scope['user'].is_anonymous:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'notify':noti
                }
            )

            
        
    async def disconnect(self, close_code):
        # Leave room group
        if self.scope['user'].is_anonymous:
            await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
      

            # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        if event['notify']:
            notify = event['notify']

            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'type': "chat_message",
                'noti': notify,
            }))
    

    @database_sync_to_async
    def write_message(self,sender_id,message,room):
        usermessages(sender_id=sender_id,reciever=room,content=message).save()

    @database_sync_to_async
    def get_messages(self,room):
        messages = usermessages.objects.filter(reciever=room)
        ak=[]
        for message in messages:
            ak.append(message.content)
        return ak

    @database_sync_to_async
    def write_status(self,stat):
        user= User.objects.get(id=self.scope['user'].id)
        if stat == True: 
            user.status="Online"
        else:
            user.status="Offline"
        user.save()
    
    @database_sync_to_async
    def get_name(self):
        return User.objects.get(id=self.scope['user'].id).username
    
    @database_sync_to_async
    def get_notify(self):
        arr={}
        mc = notifications.objects.filter(User_id=self.scope['user'].id)
        for lk in mc:
            if not contacts.objects.filter(channel=lk.channel):
                if lk.channel not in arr:
                    sk = {f"{lk.channel}":[notifications.objects.filter(User_id=self.scope['user'].id,channel=lk.channel).count(),"group"]}
                    arr.update(sk)
                else:
                    continue
            else:
                yu = contacts.objects.get(User_id=self.scope['user'].id,channel=lk.channel).contact
                if yu not in arr:
                    sk = {f"{yu}":[notifications.objects.filter(User_id=self.scope['user'].id,channel=lk.channel).count(),"contact"]}
                    arr.update(sk)
                else:
                    continue
        
        return arr








class ChatConsumer2(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_'
        if self.scope['user'].is_anonymous:
            await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
            return
        
        else:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

        await self.accept()
        await self.write_status(True)
        if not self.scope['user'].is_anonymous:
            username = await self.get_name()

        if not self.scope['user'].is_anonymous:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'username': username,
                    'status': "Online"
                }
            )

        
    async def disconnect(self, close_code):
        # Leave room group
        if self.scope['user'].is_anonymous:
            await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        if not self.scope['user'].is_anonymous:
            username = await self.get_name()
            await self.write_status(False)
        if not self.scope['user'].is_anonymous:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'username': username,
                    'status': "Offline"
                }
            )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        status = text_data_json['status']
        if status=="unknown":
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notify',
                'room': text_data_json['roomname'],
                'message':text_data_json['message']
            }
        )
        else:
            username = text_data_json['username']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'username': username,
                    'status': status
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        username = event['username']
        status = event['status']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': "chat_message",
            'username': username,
            'status':status
        }))
    

    async def notify(self, event):
        room = event['room']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': "notify",
            'room': room,
            'message':event['message']
        }))

    async def newcontact(self, event):
        room = event['room']
        if self.scope['user'].id!=int(event['id']):
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'type':'xyz',
                'room': room,
                'message':event['message']
            }))

    
        
    

    @database_sync_to_async
    def write_message(self,sender_id,message,room):
        usermessages(sender_id=sender_id,reciever=room,content=message).save()

    @database_sync_to_async
    def get_messages(self,room):
        messages = usermessages.objects.filter(reciever=room)
        ak=[]
        for message in messages:
            ak.append(message.content)
        return ak

    @database_sync_to_async
    def write_status(self,stat):
        user= User.objects.get(id=self.scope['user'].id)
        if stat == True: 
            user.status="Online"
        else:
            user.status="Offline"
        user.save()
    
    @database_sync_to_async
    def get_name(self):
        return User.objects.get(id=self.scope['user'].id).username




class ChatConsumer3(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
        
        else:
            self.room_name = self.scope['url_route']['kwargs']['room_name']+"setting"
            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

        await self.accept()
        await self.write_status(self.scope['url_route']['kwargs']['room_name'],True)

    async def disconnect(self, close_code):
        # Leave room group
        await self.write_status(self.scope['url_route']['kwargs']['room_name'],False)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        if int(event['id'])!=self.scope['user'].id:
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'username': username
            }))

    @database_sync_to_async
    def write_message(self,sender_id,message,room):
        usermessages(sender_id=sender_id,reciever=room,content=message).save()

    @database_sync_to_async
    def get_messages(self,room):
        messages = usermessages.objects.filter(reciever=room)
        ak=[]
        for message in messages:
            ak.append(message.content)
        return ak

    @database_sync_to_async
    def write_status(self,room,stat):
        user= User.objects.get(id=self.scope['user'].id)
        if stat == True: 
            user.status="Online"
        else:
            user.status="Offline"
        user.save()









    


