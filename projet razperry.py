import utime
import urequests
import network
import machine
from machine import Pin ,ADC
ldr = ADC(28)
sensor = Pin(0, Pin.IN)
signal = 0
trig = Pin(1 ,Pin.OUT ,value = 0)
echo = Pin(2, Pin.IN)
def ultrason():
  Ton = Toff = distance = 0
  trig.off()
  trig.on()
  utime.sleep_us(10)
  trig.off()
  
  while echo.value() == 0 :
   Toff = utime.ticks_us()
while echo.value() == 1 :
  Ton = utime.ticks_us()
  t = (Ton -Toff) / 2 
distance = int(t * 0.034)


SERVER_ADDRESS = "https://api.tago.io/data"
CONTENT_HEADER = "application/json"
TOKEN_HEADER = "6eaa40d3-98a6-4aae-8088-79bc643f7cf0" # Replace with your Tago.
WIFI_SSID = "Airbox-B6B8"
WIFI_PASSWORD = "qynL7GcFbWrd"
def connect_to_wifi():
   wlan = network. WLAN (network.STA_IF)
   wlan.active(True)
if not wlan.isconnected():
   print("Connecting to Wi-Fi...")
   wlan.connect(WIFI_SSID, WIFI_PASSWORD)
while not wlan.isconnected():
    pass
print("Connected to Wi-Fi:", wlan.ifconfig())
def send_data_to_tagoio(variable, value, unit): payload = {
"variable": variable,
"value": value,
"unit": unit,
}
headers = {
"Content-Type": CONTENT_HEADER,
"Device-Token": TOKEN_HEADER
}
response = urequests.post(SERVER_ADDRESS, json=payload, headers=headers)

def main():
  connect_to_wifi()
while True:
  signal = sensor.value()
  d = ultrason()
  light = int((ldr.read_u16()) * (100 / 65536))
  print(light)
  response_light = send_data_to_tagoio("light", light, "%")
  print("light Data sent:", response_light.text)
  response_light.close()
  utime.sleep_ms (30) # Delay between measurements and data sending
if _name_ == "__main__": main()