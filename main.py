# V0.1: 24.03.2026
# Hagen Jaeger
# 21Sound

# Script to read several signals from an EDC15p+ ECU (Sharan 1.9 TDI)
# and control the electric throttle pedal (TPM) to reach a constant
# Engine RPM --> Car can be used to drive a dyno / power generator

import board, busio
import adafruit_mcp4728
import time

i2c = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp4728.MCP4728(i2c)

mcp.channel_c.normalized_value = 0.0
mcp.channel_d.normalized_value = 0.0

for i in range(10000):
    # alle Kanäle aktiv, Vref = VDD, Gain = 1x
    mcp.channel_a.normalized_value = (100*i%1000) / 1000.0
    mcp.channel_b.normalized_value = (100*i%1000) / 1000.0

mcp.channel_a.normalized_value = 0.0
mcp.channel_b.normalized_value = 0.0
mcp.channel_c.normalized_value = 0.0
mcp.channel_d.normalized_value = 0.0

print("Done")