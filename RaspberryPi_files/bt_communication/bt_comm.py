import asyncio
from bleak import BleakClient, BleakScanner
 
DEVICE_NAME = "ESP32_LED"
CHARACTERISTIC_UUID = "abcd1234-ab12-cd34-ef56-1234567890ab"
 
 
async def main():
    print("Scanning for devices...")
    devices = await BleakScanner.discover(timeout=10.0)
 
    esp32 = None
    for d in devices:
        print(f"Found: {d.name} ({d.address})")
        if d.name == DEVICE_NAME:
            esp32 = d
 
    if esp32 is None:
        print(f"Could not find a device named '{DEVICE_NAME}'")
        return
 
    print(f"Connecting to {esp32.address}...")
    async with BleakClient(esp32.address) as client:
        print("Connected!")
 
        # Send a few test messages
        test_messages = ["1;255;0;0;0", "2;0;255;0;0", "3;0;0;255;0", "4;255;0;0;0", "5;0;255;0;0", "6;0;0;255;0"]
 
        for msg in test_messages:
            print(f"Sending: {msg}")
            await client.write_gatt_char(CHARACTERISTIC_UUID, msg.encode())
            await asyncio.sleep(5)
 
    print("Disconnected.")
 
 
if __name__ == "__main__":
    asyncio.run(main())