import asyncio
import websockets
from aioconsole import ainput

async def send_message():
    uri = "ws://localhost:8000/ws"  # WebSocket server URI
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await ainput("Enter a message (Ctrl-C to exit): ")  # Asynchronous input
                await websocket.send(message)  # Send the message to the server
            except KeyboardInterrupt:
                print("Exiting...")
                break

async def main():
    await send_message()

asyncio.run(main())
