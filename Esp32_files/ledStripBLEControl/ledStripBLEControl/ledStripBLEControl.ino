#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <Adafruit_NeoPixel.h>

#define PIN 21
#define NUM_LEDS 144
Adafruit_NeoPixel strip(NUM_LEDS, PIN, NEO_GRBW + NEO_KHZ800);

// UUIDs - just unique identifiers, you can generate your own
// at https://www.uuidgenerator.net/ or keep these for testing
#define SERVICE_UUID        "12345678-1234-1234-1234-123456789abc"
#define CHARACTERISTIC_UUID "abcd1234-ab12-cd34-ef56-1234567890ab"

// This class defines what happens when the Pi writes to our characteristic.
// "Callbacks" = functions that get called automatically in response to events,
// rather than being called directly by your code.
class MyCallbacks: public BLECharacteristicCallbacks {
  // onWrite() is called automatically whenever the connected device
  // writes a new value to this characteristic.
  void onWrite(BLECharacteristic *pCharacteristic) {
    String value = pCharacteristic->getValue();
  
    if (value.length() > 0) {
      int nb_leds, r, g, b, w;
      sscanf(value.c_str(), "%d;%d;%d;%d;%d", &nb_leds, &r, &g, &b, &w);
      
      Serial.print("Received: ");
      Serial.println(value);

      for (int i = 0; i < nb_leds; i++) {
        strip.setPixelColor(i, strip.Color(r, g, b, w)); // R, G, B, W
      }
      strip.show();
    }
  }
};

void setup() {
  strip.begin();
  strip.show(); // Makes sure every pixel is off
  Serial.begin(115200);
  Serial.println("Starting BLE work!");

  // Give the device a name - this is what shows up when the Pi scans
  BLEDevice::init("ESP32_LED");

  // Create the server (this ESP32 acts as a BLE peripheral/server)
  BLEServer *pServer = BLEDevice::createServer();

  // Create a service - the "folder" that holds our characteristic
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create a characteristic inside that service, with WRITE permission
  // so the Pi can send data to it
  BLECharacteristic *pCharacteristic = pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_WRITE
  );

  // Attach our callback class - this is what gets triggered on writes
  pCharacteristic->setCallbacks(new MyCallbacks());

  // Start the service and start advertising so the Pi can find us
  pService->start();
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->start();

  Serial.println("BLE ready, waiting for connections...");
}

void loop() {
  // Nothing needed here - everything happens via the callback
  delay(1000);
}
