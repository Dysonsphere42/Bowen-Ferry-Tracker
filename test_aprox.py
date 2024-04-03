import asyncio
import websockets
import json
from datetime import datetime, timezone

destination = 0.06003
zero = -123.271674

# cutoffs
bowen_docking_cutoff = 49.379349452706606
horseshoebay_docking_cutoff_x = 49.37679093807069
horseshoebay_docking_cutoff_y = -123.27215086024584

to_bowen_heading_cutoff = 180

print('imports completed')


def print_status(lat, lon, heading, speed):
    if speed > 0:
        if lat > bowen_docking_cutoff:
            return 'Docked at bowen'
        else:
            return 'Docked at Horseshoe Bay'
    elif lat > bowen_docking_cutoff and heading > to_bowen_heading_cutoff:
        return 'Docking at Bowen'


def round5(x, base=5):
    return base * round(x/base)


async def connect_ais_stream():


    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": "b40c8fe9fb22dffe43ef1d613d508f998c10c9b8",  # Required !
                             "BoundingBoxes": [[[49.401176, -123.346054], [49.364558, -123.256654]]],
                             "FiltersShipMMSI": ["316001247"],
                             "FilterMessageTypes": ["PositionReport"]}

        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message["MessageType"]

            if message_type == "PositionReport":
                # the message parameter contains a key of the message type which contains the message itself
                ais_message = message['Message']['PositionReport']
                lon = ais_message['Longitude']
                relative_lon = lon - zero
                heading = ais_message['TrueHeading']
                sog = ais_message['Sog']

                progress = abs(round5((relative_lon / destination) * 100))

if __name__ == "__main__":
    asyncio.run(asyncio.run(connect_ais_stream()))
