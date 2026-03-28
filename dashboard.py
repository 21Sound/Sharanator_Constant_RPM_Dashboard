from flask import Flask, Response, render_template_string
import can
import time
import json
import os

os.system("sudo ip link set can0 down")
os.system("sudo ip link set can0 up type can bitrate 500000")

app = Flask("Sharanator Dashboard")

# CAN-Interface öffnen
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# ------------------------------------------------------------
# HTML wird direkt eingebettet (du kannst es auch aus Datei laden)
# ------------------------------------------------------------
with open("dashboard.html", "r", encoding="utf-8") as f:
    html_page = f.read()

@app.route("/")
def index():
    return render_template_string(html_page)

# ------------------------------------------------------------
# Server-Sent Events Stream
# ------------------------------------------------------------
@app.route("/stream")
def stream():
    def event_stream():
        while True:
            msg = bus.recv(timeout=0.01)
            if msg is None:
                continue

            # Beispiel: du musst hier deine echten CAN-IDs eintragen
            if msg.arbitration_id == 0x280:   # Pedal

                pedalPercent = msg.data[5] * 100.0 / 0xFA

                engineRPM = ( (msg.data[3]<<8) + msg.data[2] ) * 0.25

                boost = 0.0

                payload = {
                    "pedal": pedalPercent,
                    "rpm": engineRPM,
                    "boost": boost
                }

                yield f"data: {json.dumps(payload)}\n\n"

                time.sleep(0)

    return Response(event_stream(), mimetype="text/event-stream")

# ------------------------------------------------------------
# Server starten
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)