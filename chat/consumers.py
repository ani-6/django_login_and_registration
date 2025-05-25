import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.user = self.scope["user"]

        usernames = sorted([self.user.username, self.other_username])
        self.room_name = f"chat_{usernames[0]}_{usernames[1]}"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get('type') == 'fetch_recent':
            await self.send_recent_messages()
            return

        message = data.get('message')
        if not message:
            return

        other_user = await sync_to_async(User.objects.get)(username=self.other_username)

        # Save the message
        msg_obj = await sync_to_async(Message.objects.create)(
            sender=self.user, receiver=other_user, content=message
        )

        # Fetch sender's display name and avatar URL
        @sync_to_async
        def get_user_info(user_id):
            user = User.objects.select_related("user_profile").get(id=user_id)
            return user.first_name, user.user_profile.thumbnail_url

        sender_name, avatar_url = await get_user_info(self.user.id)

        # Send the message to both users in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'sender_name': sender_name,
                'sender_avatar': avatar_url,
                'timestamp': msg_obj.timestamp.isoformat(),
            }
        )


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sender_name': event['sender_name'],
            'sender_avatar': event['sender_avatar'],
            'timestamp': event['timestamp'],
        }))

    async def send_recent_messages(self, limit=20):
        @sync_to_async
        def get_last_messages():
            return Message.objects.filter(
                (Q(sender=self.user, receiver__username=self.other_username) |
                Q(sender__username=self.other_username, receiver=self.user))
            ).select_related('sender__user_profile').order_by('-timestamp')[:limit][::-1]

        messages = await get_last_messages()

        for msg in messages:
            await self.send(text_data=json.dumps({
                'message': msg.content,
                'sender': msg.sender.username,
                'sender_name': msg.sender.first_name,
                'sender_avatar': msg.sender.user_profile.thumbnail_url,
                'timestamp': msg.timestamp.isoformat(),
            }))
