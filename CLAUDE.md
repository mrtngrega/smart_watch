# smart_watch

Tinkering with the user's smartwatches from the PC. Repo: github.com/mrtngrega/smart_watch (public).

## Amazfit GTS 4 Mini (active)

Zepp OS. For watch faces, mini-apps or Gadgetbridge; no firmware flashing. Nothing done on it yet.

Seen 2026-11-14 (Windows PnP, read-only, no connection made): it is paired with the PC as a BLE device ("Amazfit GTS 4 Mini", status OK, address FEB11C3AED0F). Its GATT services: standard battery (180F), heart rate (180D), alert notification (1811), device info (180A), HID consumer control (1812, the watch can act as a media remote), plus Huami vendor services FEE0, FEE1, 3802, CC353442-BE58-4EA2-876E-11D8D6976366 and 00001530-0000-3512-2118-0009AF100700. From memory, not checked: FEE0/FEE1 carry Huami's auth and data channel (what Gadgetbridge uses), and 1530-... is the firmware-update (DFU) service. Never write to the DFU service (brick risk).
Screen (Zepp's Device Basic Information table): 336x384 px portrait, corner radius 80 (unit not stated, read as px), Zepp OS 1.0, watch face preview image 228x260.

Watch face work (`watchface/`): `mockups/make_mockups.py` draws the static SVG mockups (A, B, C rough ideas; D is the user's pick). `preview/index.html` is a live page with the real time: D (A's ticks with 3 small ticks between hours and A's hands, big digital time and date at the bottom, chrome accent on the date, second hand and cap) and E (chrome ticks whose shine turns with the second hand, pointed see-through liquid-glass hands). Not built for the watch yet; the chrome, glass and moving shine would need pre-rendered images there (Zepp OS draws flat colours, from memory, not checked).

From memory, not checked: Zepp OS has watch-face tools and a JS mini-app SDK (developer mode); Gadgetbridge supports it (needs an auth key from the Zepp app); there's no custom firmware.

## ARMODD Wr3 (shelved 2026-11-14)

The user stopped this one. Only the useful findings are kept, in `docs/armodd-wr3/`:
- `protocol.md`: BLE command channel and the known commands, from GloryFit 4.0.12 decompiled.
- `gatt-dump.txt`: its full list of BLE services.

Lessons worth keeping:
- Realtek chip, closed firmware, no custom firmware. The OTA/DFU services are never written (a brick risk).
- The watch only advertises while its screen is on (15 s max), and BLE connects from Windows were flaky: 2 out of about 8 tries worked.
- Windows paired it as a classic audio/call device too; that link may block LE. It is no longer paired with the PC.
- GloryFit can't run on Windows (emulators get no Bluetooth).
- bleak on Windows: find the device by scanning first (`find_device_by_address`); connecting by address alone fails. PowerShell 5.1 can't subscribe to WinRT events, so use Python for BLE.
- Blood pressure on such watches is a light-sensor estimate, not a real measurement.

The removed Python tools (scan, listen, cmd, unpair, headset-off, gatt-dump) are in git history at commit e589614.
