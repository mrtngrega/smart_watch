# smart_watch

Tinkering with the user's smartwatches from the PC. Repo: github.com/mrtngrega/smart_watch (public).

## Amazfit GTS 4 Mini (active)

Zepp OS. For watch faces, mini-apps or Gadgetbridge; no firmware flashing. Nothing done on it yet.

Seen 2026-11-14 (Windows PnP, read-only, no connection made): it is paired with the PC as a BLE device ("Amazfit GTS 4 Mini", status OK, address FEB11C3AED0F). Its GATT services: standard battery (180F), heart rate (180D), alert notification (1811), device info (180A), HID consumer control (1812, the watch can act as a media remote), plus Huami vendor services FEE0, FEE1, 3802, CC353442-BE58-4EA2-876E-11D8D6976366 and 00001530-0000-3512-2118-0009AF100700. From memory, not checked: FEE0/FEE1 carry Huami's auth and data channel (what Gadgetbridge uses), and 1530-... is the firmware-update (DFU) service. Never write to the DFU service (brick risk).
Screen (Zepp's Device Basic Information table): 336x384 px portrait, corner radius 80 (unit not stated, read as px), Zepp OS 1.0, watch face preview image 228x260.

Watch face work (`watchface/`): `mockups/make_mockups.py` draws the static SVG mockups (A, B, C rough ideas; D is the user's pick). `preview/index.html` is a live page with the real time: D (A's ticks with 3 small ticks between hours and A's hands, big digital time and date at the bottom, chrome accent on the date, second hand and cap) and E (solid white ticks, numbers 12/3/6/9 and date, pointed see-through liquid-glass hands). E is the user's final design (2026-11-19).

Zepp project "Glass" (design E) in `watchface/zepp/`:
- `tools/make_assets.py` draws every image into `assets/gts4-mini/` (dial, AOD dial, glass and AOD hands, second hand, cap, Segoe UI digits/weekdays/months, preview/icon). Re-run it after design changes; sizes it prints are hard-coded in `watchface/index.js`.
- `app.json`: configVersion v2, target `gts4-mini`, deviceSource 246 + 247 (from Zepp's device table).
- Zeus CLI 1.10.2 is a local devDependency: `npx zeus build` works (makes `dist/*.zab`). `zeus create` and `zeus dev` prompt interactively, so run them in Harv's terminal (terminal_run), not in a background shell; `zeus dev` asks for the simulator host, answer 127.0.0.1. `zeus dev` rewrites `.gitignore`.
- Simulator 2.1.2 is installed per-user (`AppData\Local\Programs\simulator`, installer unsigned, from Zepp's docs link); the user logged in with a Zepp account; the GTS 4 Mini v1.0.3 (OS 1.0) emulator is downloaded. The simulator's Screenshot button saves the watch screen to Downloads (`zepp_screenshot_*.png`).
- Status: built and installed in the emulator ("Glass" shows in the simulator's app list, no errors in its console), but the emulator keeps showing its built-in face. A long press from a script didn't open the face picker, and clicking in the emulator window grabs the mouse (Ctrl+Alt+G releases it). Open question: how to make the emulator show an installed face. Tried 2026-11-19: the Home key (with the emulator window focused) opens its App List, which shows only "Settings"; a mouse click on it didn't open it. Next: open Settings with Enter and look for a watch-face option.
- Not checked yet: the 1.0 docs' always-on constant (code falls back from ONLY_AOD to ONAL_AOD), the week order (images are Monday first), where IMG_TIME anchors its digits.

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
