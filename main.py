# V0.1: 24.03.2026
# Hagen Jaeger
# 21Sound

# Script to read several signals from an EDC15p+ ECU (Sharan 1.9 TDI)
# and control the electric throttle pedal (TPM) to reach a constant
# Engine RPM --> Car can be used to drive a dyno / power generator

import board, busio
import adafruit_mcp4728

i2c = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp4728.MCP4728(i2c)

# Vref auf VDD (5V) setzen
mcp.channel_a.vref = adafruit_mcp4728.Vref.VDD
mcp.channel_b.vref = adafruit_mcp4728.Vref.VDD
mcp.channel_c.vref = adafruit_mcp4728.Vref.VDD
mcp.channel_d.vref = adafruit_mcp4728.Vref.VDD

mcp.channel_a.normalized_value = 0.99
mcp.channel_b.normalized_value = 0.99
mcp.channel_c.normalized_value = 0.0
mcp.channel_d.normalized_value = 0.0

print("Done")