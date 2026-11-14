# smart_watch

Customizing a cheap ARMODD Wr3 smartwatch (Realtek Bee-series chip, BLE address 78:02:B7:28:B5:19, companion app GloryFit): strip it down to what the user wants, through the app's settings first. Possibly a reverse-engineered BLE protocol so a small PC/phone tool can sync time, steps and heart rate without the vendor app. The user has a second, similar watch that may be used for firmware experiments (the ARMODD stays untouched by firmware work).

Repo: github.com/mrtngrega/smart_watch (public; renamed from armodd-watch on 2026-11-14). The local folder is still named armodd-watch until the chat that holds it is closed, then rename it to smart_watch.

## Wanted features (the user's list, 2026-11-14)

Keep only: time, date and similar, blood pressure, heart rate, step counting. Everything else off or hidden. Also a custom watch face made with Harv.

## Known facts

- Watch shows up on Windows as "ARMODD Wr3 (ID-B519)": paired as Bluetooth audio/calls device (HFP, A2DP) plus BLE with 10 services (battery 0x180F and vendor ones).
- Realtek firmware is closed; no public custom firmware. Firmware flashing over BLE can brick it, so firmware work only on the second watch, only with the user's OK.
- Blood pressure on such watches is a light-sensor estimate, not a real measurement.

## Status

Started 2026-11-14. The user unpaired the watch from the phone and wants full control from the PC (GloryFit can't run on Windows: emulators get no Bluetooth). The PC connects over BLE (no pairing needed), reads battery (reports 100%, maybe not trustworthy) and can subscribe to all vendor notify channels; the watch sends nothing unprompted (20 s listen). The GloryFit custom dial only allows background and font colour.

Next (after the weekly plan reset, Tue 17 Nov): download the GloryFit Android APK into its own folder, decompile it with jadx (Java 25 is installed) and read the command format (time sync, steps, heart rate, settings, watch-face upload), then build our own PC tool.

## Gotchas

- The watch stops advertising when asleep (screen timeout max 15 s): wake it before connecting; a paired watch is "unreachable" with the screen off.
- BLE connects are flaky (2026-11-14): worked twice (paired, awake), timed out 5 times even when the watch was visible, also with a 60 s limit. Unpaired never worked. During the last failure Windows' classic headset link (HFP/A2DP) to the watch was CONNECTED; suspect it blocks the LE link. Next try: disable the watch's audio services in Windows (admin), then connect.
- bleak on Windows: scan for the device first (`find_device_by_address`), connecting by address alone fails with "not found".
- Windows PowerShell 5.1 can't subscribe to WinRT events (no BLE scanning/notifications there); use the Python tools.

## Stack

Python 3.14 + bleak 3.1 in `.venv` (gitignored). `tools/gatt-dump.ps1` is the older read-only PowerShell dump.

## Commands

- `.venv/Scripts/python tools/scan.py 12`: scan for BLE devices, marks the watch.
- `.venv/Scripts/python tools/listen.py 20`: connect, read battery, print every notification for 20 s.
