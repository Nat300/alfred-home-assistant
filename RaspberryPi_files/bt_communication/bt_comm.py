import asyncio
import threading
from bleak import BleakClient, BleakScanner


class BluetoothManager:
    """
    Wraps bleak's async BLE API behind a synchronous interface.

    All asyncio usage is contained in this file: a dedicated background
    thread runs its own event loop, and every public method blocks the
    calling thread until the corresponding coroutine completes. Callers
    elsewhere in the project never need to know asyncio is involved.
    """

    def __init__(self):
        self.client = None
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def _run(self, coro, timeout=None):
        """Schedule a coroutine on the background loop and block until it's done."""
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result(timeout)

    # ---- internal coroutines (private, only called from within this file) ----

    async def _find_device(self, device_name, timeout: float = 5.0):
        print("Scanning for devices...")
        devices = await BleakScanner.discover(timeout=timeout)

        device = None
        for d in devices:
            print(f"Found: {d.name} ({d.address})")
            if d.name == device_name:
                device = d

        if device is None:
            print(f"Could not find a device named '{device_name}'")
            return None

        return device

    async def _connect(self, device=None, device_name: str = None):
        if device is None and device_name is not None:
            device = await self._find_device(device_name)
        if device is None:
            return None
        print(f"Connecting to {device.address}...")
        self.client = BleakClient(device)
        await self.client.connect()
        print("Successfully connected!")
        return self.client

    async def _write_to_characteristic(self, message, characteristic_uuid):
        print(f"Sending: {message}")
        await self.client.write_gatt_char(characteristic_uuid, message.encode())

    async def _disconnect(self):
        if self.client is not None:
            await self.client.disconnect()
            print("Disconnected.")

    # ---- public, synchronous API ----------------------------------------------

    def find_device(self, device_name, timeout: float = 5.0):
        return self._run(self._find_device(device_name, timeout))

    def connect(self, device=None, device_name: str = None):
        return self._run(self._connect(device, device_name))

    def write_to_characteristic(self, message, characteristic_uuid):
        return self._run(self._write_to_characteristic(message, characteristic_uuid))

    def disconnect(self):
        return self._run(self._disconnect())

    def shutdown(self):
        """Stop the background event loop and join its thread. Call on full app shutdown."""
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join(timeout=2)
