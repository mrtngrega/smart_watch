"""Connect to the watch, read battery, subscribe to every notify/indicate characteristic and print what arrives.

Passive: the only writes are the standard notification switches (CCCD).
"""
import asyncio
import sys
import time

from bleak import BleakClient, BleakScanner

WATCH = "78:02:B7:28:B5:19"
BATTERY = "00002a19-0000-1000-8000-00805f9b34fb"


async def main(seconds: float) -> None:
    dev = await BleakScanner.find_device_by_address(WATCH, timeout=20)
    if dev is None:
        sys.exit("watch not advertising")
    async with BleakClient(dev, timeout=20) as client:
        print("connected, mtu", client.mtu_size)
        print("battery", (await client.read_gatt_char(BATTERY))[0], "%")
        t0 = time.monotonic()

        def handler(char):
            def cb(_, data: bytearray):
                print(f"{time.monotonic() - t0:6.2f}s {char.uuid[4:8]} {data.hex(' ')}")
            return cb

        for svc in client.services:
            for char in svc.characteristics:
                if {"notify", "indicate"} & set(char.properties):
                    try:
                        await client.start_notify(char, handler(char))
                        print("listening", char.uuid)
                    except Exception as e:  # some need pairing; note and go on
                        print("cannot listen", char.uuid, type(e).__name__, e)
        await asyncio.sleep(seconds)


asyncio.run(main(float(sys.argv[1]) if len(sys.argv) > 1 else 20))
