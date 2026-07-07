import asyncio
import json
import websockets

# Speichert die Räume: { raum_id: { websocket: name, websocket: name } }
CHANNELS = {}

async def handle_client(websocket):
    client_room = None
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")
            
            if action == "join":
                room_id = data["room_id"]
                name = data["name"]
                client_room = room_id
                
                if room_id not in CHANNELS:
                    CHANNELS[room_id] = {}
                
                # Client zum Raum hinzufügen
                CHANNELS[room_id][websocket] = name
                print(f"[{room_id}] {name} ist beigetreten.")
                
                # Benachrichtigung an alle im Raum
                notification = json.dumps({"sender": "System", "text": f"{name} hat den Chat betreten."})
                await asyncio.gather(*[user.send(notification) for user in CHANNELS[room_id]])
                
            elif action == "message":
                if client_room and client_room in CHANNELS:
                    sender_name = CHANNELS[client_room].get(websocket, "Unbekannt")
                    payload = json.dumps({"sender": sender_name, "text": data["text"]})
                    
                    # Nachricht an alle Teilnehmer im selben Raum senden
                    await asyncio.gather(*[user.send(payload) for user in CHANNELS[client_room]])

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Bereinigen, wenn der Client die Verbindung trennt
        if client_room and client_room in CHANNELS and websocket in CHANNELS[client_room]:
            name = CHANNELS[client_room].pop(websocket)
            print(f"[{client_room}] {name} hat die Verbindung getrennt.")
            if CHANNELS[client_room]:
                notification = json.dumps({"sender": "System", "text": f"{name} hat den Chat verlassen."})
                await asyncio.gather(*[user.send(notification) for user in CHANNELS[client_room]])
            else:
                del CHANNELS[client_room]

async def main():
    # Startet den Server auf Port 8765
    server = await websockets.serve(handle_client, "0.0.0.0", 8765)
    print("Chat-Server läuft auf Port 8765...")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())