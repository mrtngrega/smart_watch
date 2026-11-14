# ARMODD Wr3 BLE protocol (from GloryFit)

Shelved on 2026-11-14: kept as reference only.

Source: GloryFit 4.0.12 (`com.yc.gloryfit`), decompiled with jadx 1.5.6 on 2026-11-14. Main files: `com/yc/pedometer/sdk/WriteCommandToBLE.java` (commands), `com/yc/pedometer/utils/UUIDUtils.java` (UUIDs). The app bundles Realtek's DFU SDK (`com.realsil.sdk.dfu`), so the chip is Realtek.

## Channels

| Service | Write | Notify | Use |
|---|---|---|---|
| `000055ff` | `000033f1` | `000033f2` | main command channel (`writeChara`) |
| `000056ff` | `000034f1` | `000034f2` | "BLE5" channel (`writeCharaBle5`), newer/bigger commands |
| `0000180f` | | `00002a19` | standard battery |
| `0000d0ff-3c17-…`, `00006287-3c17-…`, `000002fd-3c17-…` | | | Realtek OTA/DFU (firmware update): never write |

## Commands (write to `33f1`)

| Bytes | Meaning |
|---|---|
| `A1` | read firmware version |
| `A2` | read battery |
| `A3 YY YY MM DD hh mm ss` | set time (year big-endian, month 1-12) |
| `C7 02 01/00` | blood-pressure automatic test interval on/off |
| `CD 01` | read UI resource version |

Replies arrive as notifications on `33f2`; their format is still to be read (the parser is the class handling `ONLY_READ_UUID`).

The Python BLE tools (scan, listen, cmd, unpair) were removed when the watch was shelved; they are in git history at commit e589614.

Not yet looked up: steps, heart rate, settings (raise-to-wake, screen timeout), watch-face upload.
