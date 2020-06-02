from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json


class EchoConsumer(WebsocketConsumer):
    """
        Get data text and send it to client
    """
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            self.send(text_data=text_data+' - sent by server')
        

        
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

    async def chat_message(self, event):
        # import pdb; pdb.set_trace()
        message = event['message']

        await self.send(text_data=message)

