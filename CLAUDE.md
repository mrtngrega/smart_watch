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

Started 2026-11-14. Nothing built yet. Next: debloat via GloryFit settings, then the custom face, then (optional) BLE protocol work.

## Stack

Not decided yet.

## Commands

None yet.
