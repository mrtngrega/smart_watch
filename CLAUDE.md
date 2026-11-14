# smart_watch

Tinkering with the user's smartwatches from the PC. Repo: github.com/mrtngrega/smart_watch (public).

## Amazfit GTS 4 Mini (active)

Zepp OS. For watch faces, mini-apps or Gadgetbridge; no firmware flashing. Nothing done on it yet.
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
