import json
import re

from main import models

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.pattern = re.compile("^#.+")

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        match = re.search(self.pattern, message)
        message_args = {}
        if match is not None:
            advert = await self.get_advert(match[0][1:])
            if advert is not None:
                if not advert.is_sold:
                    message_args["title"] = advert.title
                    message_args["description"] = advert.description
                    message_args["price"] = advert.price
                else:
                    message_args["sold"] = 'Продано'

            else:
                message_args["nofound"] = 'Не найдено'

            await self.send(text_data=json.dumps({"message": message_args}))
        else:
            message_args["nofound"] = 'Не найдено'
            await self.send(text_data=json.dumps({"message": message_args}))

    @database_sync_to_async
    def get_advert(self, message):
        return models.CarAdvert.objects.filter(title__icontains=message).first()
