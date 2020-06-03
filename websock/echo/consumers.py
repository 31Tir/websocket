from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.consumer import AsyncConsumer
import json


class EchoConsumer(WebsocketConsumer):
    """
        Get data text and send it to client
    """
    def connect(self):
        self.room_id = "echo_1"

        async_to_sync(self.channel_layer.group_add)(
            self.room_id,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_id,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            self.send(text_data=text_data+' - sent by server')
        
    def echo_message(self, event):
        message = json.loads(event['message'])
        self.send(text_data=' {0} : {1}  ===>  {2}'.format(message['sender'], message['text'], message['receiver'] ))

    
class ChatConsumer(AsyncWebsocketConsumer):
    """
        for connect create group and add user to this
        and for disconnect delete that group
    """
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['username']
        self.group_name = f"chat_{self.user_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """
            Get and send message to user group name
        """
        if text_data:
            text_data_json = json.loads(text_data)
            username = text_data_json['receiver']
            user_group_name = f"chat_{username}"

            await self.channel_layer.group_send(
                user_group_name,
                {
                'type': 'chat_message',
                'message': text_data
                }
            )

            await self.channel_layer.group_send(
                'echo_1',
                {
                'type': 'echo_message',
                'message': text_data
                }
            )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=message)


    