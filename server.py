# import asyncio
# import websockets
# import time

# async def send_messages(websocket=None, path=None):
# 	async for message in websocket:
#             print(message)
#             print(type(websocket))
#             async with websockets.connect('ws://127.0.0.1:1234') as conn:
#                 await conn.send("4,0.23,0.20,-10.60,0.03,-0.03,-0.03,-4.74,-49.18,-35.02")
#                 print('------ ping')
#                 time.sleep(1)

# start_server = websockets.serve(send_messages, '127.0.0.1', 1234)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
# # websocket.WebSocketApp()


# import websocket



# def on_open(ws):
#     print("Connection is opened")

# def on_message(ws, message):
#     print("Received message: ", message)

# def on_error(ws, error):
#     print("Error occured: ", error)

# # def on_close(ws, close_reason, close_):
# #     print("Connection is closed")


# ws = websocket.WebSocketApp("ws://127.0.0.1:1234",
#                             on_open = on_open,
#                             on_message = on_message,
#                             on_error = on_error)

# ws.run_forever()


import asyncio
import websockets


async def handler(websocket, path):
    while True:
        message = "4,0.23,0.20,-10.60,0.03,-0.03,-0.03,-4.74,-49.18,-35.02"
        await websocket.send(message)
        print(f'sent {message}')
        await asyncio.sleep(1)

start_server = websockets.serve(handler, 'localhost', 1234)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()