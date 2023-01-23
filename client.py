import asyncio
import websockets

async def receive_message(websocket=None, path=None):
    async with websockets.connect('ws://127.0.0.1:1234') as conn:
        await conn.send('Hello, world')
        message = await conn.recv()
        print(f"We got the message from the server: {message}")

# start_client = websockets.connect('ws://127.0.0.1:1234')
asyncio.get_event_loop().run_until_complete(receive_message())
