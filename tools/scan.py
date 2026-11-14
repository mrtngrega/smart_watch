"""Scan for BLE advertisements and print what is seen (read-only)."""
import asyncio
import sys

from bleak import BleakScanner

WATCH = "78:02:B7:28:B5:19"


async def main(seconds: float) -> None:
    found = await BleakScanner.discover(timeout=seconds, return_adv=True)
    for addr, (dev, adv) in sorted(found.items(), key=lambda kv: -kv[1][1].rssi):
        mark = "  <-- watch" if addr.upper() == WATCH else ""
        print(f"{addr} rssi={adv.rssi:4} name={adv.local_name or dev.name}{mark}")
        if addr.upper() == WATCH:
            print(f"    services={adv.service_uuids}")
            print(f"    manufacturer={ {k: v.hex() for k, v in adv.manufacturer_data.items()} }")
    if WATCH not in {a.upper() for a in found}:
        print("watch not advertising")


asyncio.run(main(float(sys.argv[1]) if len(sys.argv) > 1 else 10))
