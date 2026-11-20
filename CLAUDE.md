# smart_watch

Tinkering with the user's smartwatches from the PC. Repo: github.com/mrtngrega/smart_watch (public).

## Amazfit GTS 4 Mini (active)

Zepp OS. For watch faces, mini-apps or Gadgetbridge; no firmware flashing. The watch face "Glass" runs on it (installed 2026-11-20).

Seen 2026-11-14 (Windows PnP, read-only, no connection made): it is paired with the PC as a BLE device ("Amazfit GTS 4 Mini", status OK, address FEB11C3AED0F). Its GATT services: standard battery (180F), heart rate (180D), alert notification (1811), device info (180A), HID consumer control (1812, the watch can act as a media remote), plus Huami vendor services FEE0, FEE1, 3802, CC353442-BE58-4EA2-876E-11D8D6976366 and 00001530-0000-3512-2118-0009AF100700. From memory, not checked: FEE0/FEE1 carry Huami's auth and data channel (what Gadgetbridge uses), and 1530-... is the firmware-update (DFU) service. Never write to the DFU service (brick risk).
Screen (Zepp's Device Basic Information table): 336x384 px portrait, corner radius 80 (unit not stated, read as px), Zepp OS 1.0, watch face preview image 228x260.

Watch face work (`watchface/`): `mockups/make_mockups.py` draws the static SVG mockups (A, B, C rough ideas; D is the user's pick). `preview/index.html` is a live page with the real time: D (A's ticks with 3 small ticks between hours and A's hands, big digital time and date at the bottom, chrome accent on the date, second hand and cap) and E (solid white ticks, numbers 12/3/6/9 and date, pointed see-through liquid-glass hands). E is the user's final design (2026-11-19).

Zepp project "Glass" (design E) in `watchface/zepp/`:
- `tools/make_assets.py` draws every image into `assets/gts4-mini/` (dial with ticks 3 px from the screen edge, glass hands, thin second hand, 16 px opaque chrome cap, Segoe UI digits/weekdays/months, preview/icon). Re-run it after design changes; sizes it prints are hard-coded in `watchface/index.js`.
- `app.json`: configVersion v2, target `gts4-mini`, deviceSource 246 + 247 (from Zepp's device table).
- Zeus CLI 1.10.2 is a local devDependency: `npx zeus build` works (makes `dist/*.zab`). `zeus create` and `zeus dev` prompt interactively, so run them in Harv's terminal (terminal_run), not in a background shell; `zeus dev` asks for the simulator host, answer 127.0.0.1. `zeus dev` rewrites `.gitignore`.
- Simulator 2.1.2 is installed per-user (`AppData\Local\Programs\simulator`, installer unsigned, from Zepp's docs link); the user logged in with a Zepp account; the GTS 4 Mini v1.0.3 (OS 1.0) emulator is downloaded. The simulator's Screenshot button saves the watch screen to Downloads (`zepp_screenshot_*.png`).
- Status: built and installed in the emulator ("Glass" shows in the simulator's app list, no errors in its console), but the emulator keeps showing its built-in face. A long press from a script didn't open the face picker, and clicking in the emulator window grabs the mouse (Ctrl+Alt+G releases it). Open question: how to make the emulator show an installed face. Tried 2026-11-19: the Home key (with the emulator window focused) opens its App List, which shows only "Settings"; the user looked in its Settings and found no watch-face option. Dropped in favour of the real watch (below).
- The emulator has no watch-face picker (the user checked its Settings, 2026-11-19), so testing moved to the real watch.
- Real watch (works since 2026-11-20): Glass is installed on the GTS 4 Mini by the preview QR. Steps: Developer Mode on in the Zepp app (Profile > Settings > About > tap the Zepp icon 7 times), `npx zeus login --no-browser` (open the link in a private window, sign in, paste the final address-bar URL into the terminal; never Ctrl+C there), `npx zeus status` must show the same account as the phone's Zepp app, then `npx zeus preview -t gts4-mini` in `watchface/zepp` (run it in Harv's terminal with that cwd; elsewhere `npx zeus` runs a different package) and scan the QR (Profile > the watch > Developer Mode > scan icon top right). The line "Supported device: undefined" is cosmetic (Zeus prints `args.device`, which is empty when `-t` is used).
- Traps hit on 2026-11-19/20: (1) the account is 7019545643 (nickname mrtngrega) on both the CLI and the phone; an earlier "Martin Grega" login on the phone was the wrong one. (2) Zepp's login says "request times are too frequent" after about 6 tries; it was still blocked after 12 hours on the home IP and worked at once on a phone hotspot (so it is probably per IP; unplug ethernet, since Windows prefers it over Wi-Fi). (3) A VPN on the phone may block the transfer; keep it off. (4) After a QR scan the app lists the face with a red "Try again" when the phone-to-watch step failed. Glass failed that way with appId 1000001 (several failed tries) and installed at once with appId 1000003; an empty official face (appId 1000002) installed fine, so account, link and device numbers (246/247) were fine. The exact reason an old appId fails is not proven (a stale entry for that ID is the guess): after a failed install, use a new appId. (5) `zeus bridge` > `connect` always said "No connectable online App or Simulator" (the phone has no Bridge page, only the Developer Mode list); the QR route is the one that works. (6) Platform `name` in app.json is a free label; only deviceSource (246, 247 = GTS 4 mini) matters.
- Face state (2026-11-20, confirmed on the real watch): plain black dial (the old centre glow is gone), always-on shows the same face as the normal screen minus the second hand (about 7.4% of pixels lit; Zepp's guidance is 10%, and its guidance for plain white AOD hands is not followed; not enforced for a preview install). The second hand is drawn after the chrome cap, so it sits on top of it. The watch draws always-on about 4 px up and left of the normal screen (same every time, whole face), so `watchface/index.js` draws the always-on copy at `AOD_DX/AOD_DY = 4, 4` to cancel it; adjust those two numbers if it ever looks off. Ticks sit 3 px from the edge, so always-on may lose about 1 px at the bottom and right.
- Research notes from this session (agents read the official docs; not all re-checked): `docs/zepp-os-customization.md` (what a face can show and which system screens the user can set up himself: no custom swipe tab on this watch, the Quick Access screen is the built-in way), `docs/zepp-watchface-battery.md` (almost nothing is documented about face battery use; always-on rules), `docs/zepp-system-battery.md` (no custom firmware found, Gadgetbridge is Android only, never flash).
- Not checked yet: the weekday order (images are Monday first) and the always-on constant name on this firmware (code falls back from ONLY_AOD to ONAL_AOD); both looked right in the photos (FRI 20 NOV on Friday 20 November).

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
