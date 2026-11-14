"""Send one command (hex) to the watch's main channel and print the replies.

Usage: cmd.py a1          read firmware version
       cmd.py a2          read battery
       cmd.py time        set the watch clock to this PC's time
Only use commands listed in docs/protocol.md; never write to the OTA services.
"""
import asyncio
import datetime
import sys

from bleak import BleakClient, BleakScanner

WATCH = "78:02:B7:28:B5:19"
WRITE = "000033f1-0000-1000-8000-00805f9b34fb"
NOTIFY = "000033f2-0000-1000-8000-00805f9b34fb"


def build(arg: str) -> bytes:
    if arg == "time":
        n = datetime.datetime.now()
        return bytes([0xA3, n.year >> 8, n.year & 0xFF, n.month, n.day, n.hour, n.minute, n.second])
    return bytes.fromhex(arg)


async def main(arg: str) -> None:
    payload = build(arg)
    dev = await BleakScanner.find_device_by_address(WATCH, timeout=90)
    if dev is None:
        sys.exit("watch not advertising (wake it)")
    async with BleakClient(dev, timeout=60) as client:
        await client.start_notify(NOTIFY, lambda _, d: print("reply", d.hex(" ")))
        print("send ", payload.hex(" "))
        await client.write_gatt_char(WRITE, payload, response=True)
        await asyncio.sleep(3)


asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "a1"))
