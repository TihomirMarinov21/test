
import asyncio
import websockets
import os

PORT = int(os.environ.get("PORT", 8765))

clients = set() # erstelle eine Menge, um die verbundenen Clients zu speichern

async def handler(websocket):   # definiere asynchrone handler funktion

    clients.add(websocket)      # neue websocket verbindung wird als client zum Set hinzugefügt

    try:
        async for message in websocket:     # async endlosschleife während client verbunden ist um nachrichten des clients zu lesen

            print(f"Received: {message}")   # console log

            for client in clients:          # wenn eine nachricht kommt, wird sie an jeden verbundenen client gesendet (einschließlich Sender)
                await client.send(message)  

    except:
        pass

    finally:                                # wenn fehler, entferne client aus dem Set
        clients.remove(websocket)

async def main():                           # definiere asynchrone main function

    server = await websockets.serve(        # server erstellen mit handler, host und PORT
        handler,
        "0.0.0.0",
        PORT
    )

    print(f"Server started on port {PORT}") # console log

    await server.wait_closed()              # warte auf beenden aller verbindungen, dann schließe den server

asyncio.run(main())
