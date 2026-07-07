import asyncio
import websockets
import os

PORT = int(os.environ.get("PORT", 8765))
clients = set()

async def handler(websocket):
    clients.add(websocket)

    try:
        async for message in websocket:

            print(f"Received: {message}")

            for client in clients:
                if client != websocket:
                    await client.send(message)

    except:
        pass

    finally:
        clients.remove(websocket)

import os

PORT = int(os.environ.get("PORT", 8765))

async def main():
    server = await websockets.serve(
        handler,
        "0.0.0.0",
        PORT
    )

    print(f"Server started on port {PORT}")

    await server.wait_closed()

    print("Server started on port 8765")

    await server.wait_closed()

asyncio.run(main())
