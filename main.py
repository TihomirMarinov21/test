import asyncio
import websockets

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

async def main():
    server = await websockets.serve(
        handler,
        "0.0.0.0",
        8765
    )

    print("Server started on port 8765")

    await server.wait_closed()

asyncio.run(main())