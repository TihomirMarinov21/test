import tkinter as tk
from tkinter import messagebox
import asyncio
import threading
import json
import websockets

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Raum-Chat")
        self.websocket = None
        self.loop = None
        
        # HIER DIE SERVER-URL ANPASSEN (z.B. ws://deine-server-ip:8765)
        self.SERVER_URI = "ws://localhost:8765"

        # --- Login Maske ---
        self.login_frame = tk.Frame(root, padx=20, pady=20)
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(self.login_frame)
        self.name_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.login_frame, text="Raum-ID:").grid(row=1, column=0, sticky="w")
        self.room_entry = tk.Entry(self.login_frame)
        self.room_entry.grid(row=1, column=1, pady=5)

        self.join_btn = tk.Button(self.login_frame, text="Chatraum betreten / erstellen", command=self.start_connect)
        self.join_btn.grid(row=2, columnspan=2, pady=10)

        # --- Chat Fenster (wird erst nach Login sichtbar) ---
        self.chat_frame = tk.Frame(root, padx=10, pady=10)
        
        self.chat_box = tk.Text(self.chat_frame, state="disabled", width=50, height=20)
        self.chat_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.msg_entry = tk.Entry(self.chat_frame)
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5)
        self.msg_entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = tk.Button(self.chat_frame, text="Senden", command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT, padx=5)

    def start_connect(self):
        self.name = self.name_entry.get().strip()
        self.room_id = self.room_entry.get().strip()

        if not self.name or not self.room_id:
            messagebox.showerror("Fehler", "Bitte Name und Raum-ID eingeben!")
            return

        # Startet den Asyncio Loop in einem separaten Thread, damit das GUI nicht einfriert
        threading.Thread(target=self.start_asyncio_loop, daemon=True).start()

    def start_asyncio_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect_to_server())

    async def connect_to_server(self):
        try:
            async with websockets.connect(self.SERVER_URI) as websocket:
                self.websocket = websocket
                
                # Login-Daten senden
                join_data = json.dumps({"action": "join", "room_id": self.room_id, "name": self.name})
                await self.websocket.send(join_data)
                
                # GUI wechseln
                self.root.after(0, self.show_chat_interface)
                
                # Auf eingehende Nachrichten hören
                async for message in self.websocket:
                    data = json.loads(message)
                    display_text = f"{data['sender']}: {data['text']}\n"
                    self.root.after(0, self.append_message, display_text)
                    
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Verbindungsfehler", f"Keine Verbindung zum Server: {e}")

    def show_chat_interface(self):
        self.login_frame.pack_forget()
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        self.root.title(f"Chatraum: {self.room_id} - Angemeldet als {self.name}")

    def append_message(self, text):
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, text)
        self.chat_box.config(state="disabled")
        self.chat_box.see(tk.END)

    def send_message(self):
        msg = self.msg_entry.get().strip()
        if msg and self.websocket and self.loop:
            self.msg_entry.delete(0, tk.END)
            # Nachricht über den laufenden Asyncio-Loop senden
            payload = json.dumps({"action": "message", "text": msg})
            asyncio.run_coroutine_threadsafe(self.websocket.send(payload), self.loop)

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()