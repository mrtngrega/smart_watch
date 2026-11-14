"""Remove the watch's Windows Bluetooth pairing (classic and LE). Undo: pair it again in Windows Settings."""
import asyncio

from winrt.windows.devices.bluetooth import BluetoothDevice, BluetoothLEDevice

ADDR = 0x7802B728B519


async def main() -> None:
    for kind, cls in (("classic", BluetoothDevice), ("LE", BluetoothLEDevice)):
        dev = await cls.from_bluetooth_address_async(ADDR)
        if dev is None:
            print(kind, "not known to Windows")
            continue
        pairing = dev.device_information.pairing
        if not pairing.is_paired:
            print(kind, "not paired")
            continue
        result = await pairing.unpair_async()
        print(kind, "unpair:", result.status.name)


asyncio.run(main())
