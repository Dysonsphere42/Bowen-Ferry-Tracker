import asyncio
import websockets
import json
from datetime import datetime, timezone

async def connect_ais_stream():


    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": "b40c8fe9fb22dffe43ef1d613d508f998c10c9b8",  # Required !
                             "BoundingBoxes": [[[49.401176, -123.346054], [49.364558, -123.256654]]], # Required!
                             "FiltersShipMMSI": ["316001247"], # Optional!
                             "FilterMessageTypes": ["PositionReport"]} # Optional!

        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message["MessageType"]

            if message_type == "PositionReport":
                # the message parameter contains a key of the message type which contains the message itself
                ais_message = message['Message']['PositionReport']
                print(f"[{datetime.now(timezone.utc)}] ShipId: {ais_message['UserID']} Latitude: {ais_message['Latitude']} Longitude: {ais_message['Longitude']}")

if __name__ == "__main__":
    asyncio.run(asyncio.run(connect_ais_stream()))
