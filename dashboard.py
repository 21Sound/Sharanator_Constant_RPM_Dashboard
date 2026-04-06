from flask import Flask, Response, request, jsonify, render_template_string
import can
import time
import json
import os
import sys

params = {
"rpm_target": 1000,
"pedal_input": 0.0,
"tau_att": 0.1,
"tau_rel": 0.1,
"pedal_gain": 0.0,
"toggle_const_RPM": 0,
"toggle_emergency_off": 0,
"toggle_tbd": 0
}

print(params.keys())

print(sys.platform.lower())

if "linux" in sys.platform.lower():
    os.system("sudo ip link set can0 down")
    os.system("sudo ip link set can0 up type can bitrate 500000")

app = Flask("Sharanator Dashboard")

# CAN-Interface öffnen
if "linux" in sys.platform.lower():
    CAN_BUS_INST = can.interface.Bus(channel='can0', bustype='socketcan')

# ------------------------------------------------------------
# HTML wird direkt eingebettet (du kannst es auch aus Datei laden)
# ------------------------------------------------------------
with open("dashboard.html", "r", encoding="utf-8") as f:
    html_page = f.read()

@app.route("/")
def index():
    return render_template_string(html_page)

@app.post("/update")
def update():
    data = request.get_json()
    for key, value in data.items():
        if key in params.keys():
            params[key] = value
            #print("\n Updated params:" + str(params) + "\n")
    return jsonify(success=True)

@app.get("/values")
def values():
    return jsonify(params)

# ------------------------------------------------------------
# Server-Sent Events Stream
# ------------------------------------------------------------
@app.route("/stream")
def stream():
    def event_stream():

        pedalPercent = 0.0
        engineRPM = 0.0
        velocityKmph = 0.0
        enginePowerPercent = 0.0
        torqueNM = 0.0
        fuelPercent = 0.0
        
        canMsg = None

        while True:

            if "linux" in sys.platform.lower():
                canMsg = CAN_BUS_INST.recv(timeout=0.01)
                if canMsg is not None:
                    if canMsg.arbitration_id == 0x280:   # Pedal
                        pedalPercent = canMsg.data[5] * 100.0 / 0xFA
                        engineRPM = ( (canMsg.data[3]<<8) + canMsg.data[2] ) * 0.25
            else:
                time.sleep(0.01)
                engineRPM = params["rpm_target"]
                pedalPercent = params["pedal_input"]

            payload = {
                "pedal": pedalPercent,
                "rpm": engineRPM,
                "kmph": velocityKmph,
                "power": enginePowerPercent,
                "torque": torqueNM,
                "fuel": fuelPercent,
            }

            yield f"data: {json.dumps(payload)}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")

# ------------------------------------------------------------
# Server starten
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)