# Zepp OS 1.0 watch face: what the official docs say about battery and smoothness

Researched 2026-11-20 for the Amazfit GTS 4 Mini (Zepp OS 1.0, 336x384, deviceSource 246/247) and the "Glass" face (configVersion v2, hmUI widgets, Zeus CLI).

Sources used (primary only):
- The live Zepp docs at `docs.zepp.com`. The 1.0 docs live under `/docs/1.0/...`. Pages without `/1.0/` are the newer docs.
- The official docs repo `github.com/zepp-health/zeppos-docs` (branch main, commit 2b7b79e), folder `versioned_docs/version-1.0`. I used it to check the exact wording of the live pages.
- The official samples `github.com/zepp-health/zeppos-samples` (main, commit 7cee748), folder `watchface/1.0`.

No forums or blogs were used as evidence. Anything I could not find in those sources is marked "not verified" or "not documented".

Short form used below: `DOCS1` = `https://docs.zepp.com/docs/1.0`, `REPO1` = `https://github.com/zepp-health/zeppos-docs/blob/main/versioned_docs/version-1.0`, `SAMPLES` = `https://github.com/zepp-health/zeppos-samples/blob/main/watchface/1.0`.

## Answer in plain words

- **Almost nothing about watch face battery or performance is documented for 1.0.** There is no power budget, no limit on widget count, no limit on image count or size, and no memory limit. The only hard numbers are the AOD rules. Most of what follows is "the docs say X" or "the docs say nothing", not a measured tip.
- **What the docs do ask of the face (AOD only).**
  - Lit pixels must not exceed 10% of the screen.
  - No second hand.
  - Pure black background, white hands.
  - Keep element positions the same as in the normal mode.
  - Glass already does this in structure: it uses separate `show_level` widgets for normal and AOD, and its AOD hands have no second hand. Check the 10% figure for the AOD dial (see gaps).
- **Create widgets only for the mode that needs them (`show_level`).** The docs say a widget created with `show_level: ONLY_NORMAL` is not created in AOD. Date, week, digital time and the second hand therefore cost nothing in AOD. The docs say this reduces JS logic and errors. They do not claim a battery or speed gain.
- **Use one image per hand.** The 1.0 TIME_POINTER page warns: "Configuring multiple images may affect the Watchface performance". Use one image per hand, and keep the optional cap image to one. This is the only performance warning in the 1.0 watch face widget docs.
- **Prefer data-bound widgets to your own polling or timers.** Per the 1.0 docs, the firmware does data updates and timer recovery, and it pauses data listeners and timers when the face is not on screen. Glass uses no timers, sensors or data listeners, so it is already in the cheap case. Do not add a heart-rate `CURRENT` listener, because the docs say registering it starts continuous heart-rate measurement.
- **No documented effect, so do not expect a gain from these:**
  - Image format and colour depth. The only guidance is "24-bit or 32-bit png with RGB or RGBA".
  - Image compression and TGA conversion.
  - How the second hand is refreshed. The docs do not say whether it is per second or smooth, or what that costs.
  - The `lockscreen` and `photoscreen` flags (they are simply listed).
  - Developer-mode (QR) install versus a published install.
  - How often the system refreshes AOD.
- **Not verified.** There are no official numbers on second-hand cost, AOD refresh rate, memory use, or a developer-mode install. The only way to know is to measure on the watch, for example with the battery percentage over a fixed time with the second hand on and off. The `getPerformance` API in the newer docs reports memory, but it needs API_LEVEL 4.0, so it is not available on 1.0.

## 1. Power guidance for watch faces

**Only the AOD (always-on) rules carry numbers. They come from the 1.0 Watchface Specification.**

Source: <https://docs.zepp.com/docs/1.0/watchface/specification/> (also in `REPO1/watchface/specification.md`). Design rules, quoted:
- "Minimize the number of Watchface elements, so that the illuminated pixels do not exceed 10% of the screen."
- "Don't use the second hand on the Watchface."
- "The background color of the Watchface must be black (#000000) and the main color of the pointer must be white (#FFFFFF)."
- "Keep the pointer/digital cutting size consistent."
- "Because it is necessary to switch between the rest screen and the bright screen, the element movement should be minimized to avoid jumping during switching."
- "To ensure recognition, keep the basic time scale (not mandatory)."
- "Except time, the priority of other elements is: steps > date > weather > electricity > heart rate > others (not mandatory but basically observed)."

The same page says the Always-On Display mode "is an essential mode of a Watchface". It also says there are two kinds. The AOD either follows the current watch face, or is a style the user picks independently. A face that follows the current watch face "needs to be designed separately by the Watchface designer".

The matching design page (<https://docs.zepp.com/docs/1.0/designs/specifications/screen-off-mode/>) words the pixel rule as: "When an element on the Watchface lights up, its pixels cannot exceed 10% of the pixels of the screen." It adds these hand and digit rules:
- Remove gradients, highlights and shadows, and keep the silhouette.
- Give the hands a 1-2 px black outer border.
- Use at least a 2 px stroke for digits.
- "Add as few colors as possible" to the hands.
- A "white film" method is also allowed. It keeps some structural light and shadow in the hand.
- "When the illuminated area is less than 10%, the border area can be omitted."

**The docs do not say why the limits exist.** They do not tie the 10% figure to battery. Calling it a battery rule is an inference.

**Pages that contain no power or performance guidance (checked):**

| Topic | Page checked | Result |
|---|---|---|
| Quick start | <https://docs.zepp.com/docs/1.0/watchface/watchface-quick-start/> | none |
| Design resources | <https://docs.zepp.com/docs/1.0/watchface/design-resources/> | none (it only offers a "screen rest" reference PDF) |
| Design index | <https://docs.zepp.com/docs/1.0/designs/> | none |
| Composition | <https://docs.zepp.com/docs/1.0/designs/specifications/composition/> | none |
| app.json | <https://docs.zepp.com/docs/1.0/watchface/app-json/> | no performance or power notes |

- **Update frequency, animation and widget count:** none of the checked 1.0 pages say anything about these for watch faces. The only "animation" wording is the AOD rule about minimising element movement between modes.
- **"High power consumption watchface" flag in Watchface Maker.** The Watchface Maker release notes (v4.7.2, 1 June 2022) say: "Support high power consumption Watchface configuration, can be configured when creating and editing Watchface (Zepp OS)". Source: `https://github.com/zepp-health/zeppos-docs/blob/main/docs/guides/tools/watchface/release-note.md`. The docs never explain what the flag does or whether it exists for code-based Zeus faces. This is not verified for Glass.

## 2. Second hand, refresh, IMG_ANIM, timers, sensors (1.0)

### TIME_POINTER

Source: <https://docs.zepp.com/docs/1.0/watchface/api/hmUI/widget/TIME_POINTER/> (`REPO1/watchface/api/hmUI/widget/TIME_POINTER.mdx`).
- The page documents only the `hour_*` parameters. It says "Minute and seconds as same as above, just replace hour with minute/second."
- It has one warning, quoted: "It is recommended to configure at most one image for hour, minute and second hands. Configuring multiple images may affect the Watchface performance". The "xx_cover is an optional field" note sits next to it.
- **Not documented:** whether the second hand moves once per second or smoothly, any option to slow or disable second-hand updates, and the cost of it.
- The 1.0 page does not list `show_level` for TIME_POINTER. `show_level` is described as a generic widget option set at create time (section 4). Whether TIME_POINTER honours it is not documented on the TIME_POINTER page.
- **Official sample technique for AOD pointers.**
  - The sample calls `hmSetting.getScreenType()` and compares it with `hmSetting.screen_type.AOD`.
  - It then asks the pointer editor for the pointer config without the second hand when in AOD: `pointerEdit.getProperty(hmUI.prop.CURRENT_CONFIG, !aodModel)` (`SAMPLES/color-world/watchface/square/index.js`, around lines 820-834).
  - The editable-pointer docs say that second parameter is "whether to export the second hand property" (`REPO1/watchface/api/hmUI/widget/edit_watchface.mdx`).
  - So the AOD code path is the same file run in AOD, and the second hand is dropped there.

### IMG_POINTER

Source: `REPO1/watchface/api/hmUI/widget/IMG_POINTER.mdx`. "The widget area is full screen." It rotates one image about a centre. No performance or power notes.

### IMG_TIME

Source: <https://docs.zepp.com/docs/1.0/watchface/api/hmUI/widget/IMG_TIME/>. It is a code example with comments only. There is no refresh, anchor or performance text.

### IMG_ANIM

Source: <https://docs.zepp.com/docs/1.0/watchface/api/hmUI/widget/IMG_ANIM/>.
- Parameters include `anim_fps` ("Number of frames of animation."), `anim_size` ("The number of images."), `step` ("Frame animation step, will skip frames when greater than `1`."), and `display_on_restart` ("Whether to restart the animation when the dial resume triggers").
- `default_frame_index` is described as "Index of displayed sequence frames in power saving mode". This is the only place the 1.0 widget docs name a "power saving mode". It says nothing about AOD or battery numbers.
- No performance or battery warning on the page.
- Glass does not use IMG_ANIM.

### Timers

- **`timer.createTimer`** (<https://docs.zepp.com/docs/1.0/watchface/api/timer/createTimer/>). The signature is `(delay, repeat, callback, option) => timerId`. The example comment reads: "Create timer, delay 500ms to trigger, then execute every 1000ms." There are no notes or warnings on the page.
- **What the firmware does with timers (UI lifecycle proxy).** The 1.0 `createWidget` page (<https://docs.zepp.com/docs/1.0/watchface/api/hmUI/createWidget/>, section "UI lifecycle proxy") says: "Currently data update and timer recovery are done inside the firmware, but part of the Watchface depends on the UI lifecycle, so a new virtual control has been added to sense the lifecycle." A table on that page lists the following for the `WIDGET_DELEGATE` widget:

  | Callback | Firmware internal operations | When it fires |
  |---|---|---|
  | `resume_call` | "Resume all data listeners, resume timer." | "Watchface first start; other screens back to watchface." |
  | `pause_call` | "Pause all data listening, pause timer" | "Swipe to subscreen, notifications control center enter, access to other applications from the watchface." |

  The page also says the delegate draws nothing and is released automatically.
- **Official sample practice.** The basketball sample starts its animation timer in `resume_call` and calls `timer.stopTimer` in `pause_call` (`SAMPLES/basketball/watchface/round/index.js`). Docs-wise this is the only guidance on timers in a face.
- **Deprecation note, for the newer docs only.** The migration guide (<https://docs.zepp.com/docs/guides/version-info/migration-guide/>, Case 9) says: "1.0 timer timer module is deprecated and needs to be replaced with JS timer API". It says the upgraded API applies only to the Device App, so it does not change the 1.0 face API.

### Sensor listeners and time events

- **TIME sensor** (<https://docs.zepp.com/docs/1.0/watchface/api/hmSensor/sensorId/TIME/>). Only two events exist: `MINUTEEND` ("Events at the end of each minute") and `DAYCHANGE` ("Events at the end of each day"). The DAYCHANGE row on the page lists the value `time.event.MINUTEEND`, which looks like a copy error. There is no per-second event, and no power or performance note.
- **HEART sensor** (<https://docs.zepp.com/docs/1.0/watchface/api/hmSensor/sensorId/HEART/>). The page says registering the `CURRENT` event "enable[s] continuous heart rate measurement". It also says that if you use event callbacks you should call `removeEventListener` in the page's `onDestroy`. The page does not state a battery cost, so the cost is not verified. It is an inference that continuous measurement uses more power.

## 3. Memory, image format and widget limits

- **Image format guidance (the only one in 1.0).** The IMG widget page (<https://docs.zepp.com/docs/1.0/watchface/api/hmUI/widget/IMG/>) says: "Recommend using 24-bit or 32-bit png format images with RGB or RGBA color scheme." It adds that `w` and `h` come from the image file itself, so the widget cannot scale the image.
- **TGA, RGB565, 16-bit versus 32-bit, compression.** I searched the whole 1.0 and current docs repo for TGA, RGB565, colour depth and compression. None of these is documented. The Zeus CLI page (<https://docs.zepp.com/docs/1.0/guides/tools/cli/>) covers `zeus build`, `preview`, `dev` and `config` only. It has no image-conversion options. I found no documented build-tool setting for colour depth. Whether `zeus build` converts PNGs, and to what, is not verified. (A community tool that converts PNG to TGA exists, but I did not use it as evidence.)
- **Scaling.**
  - `designWidth` in app.json is only the base for the `px()` helper, which is `Math.ceil(x / designWidth * DEVICE_WIDTH)` (<https://docs.zepp.com/docs/1.0/guides/best-practice/multi-screen-adaption/>).
  - Glass has `designWidth` 336, which matches the screen width, so `px()` is a no-op. The docs do not say anything about scaling cost.
- **Memory limits.** None documented for 1.0 watch faces. The only memory tool is `getPerformance` in the newer docs (<https://docs.zepp.com/docs/reference/device-app-api/newAPI/app/getPerformance/>). It needs API_LEVEL 4.0, so it is not available on Zepp OS 1.0. I did not fetch that page, so this comes from a search result and is not verified.
- **Widget count and page load time.** No limit and no advice in the 1.0 docs. The only widget-count related text is "Minimize the number of Watchface elements" in the AOD rules.
- **Install-time table** (`Installation time list`) is about setting up the dev environment, not the watch.

## 4. Always-on display (AOD) behaviour on 1.0

**Constants.** `hmUI.show_level` (source: <https://docs.zepp.com/docs/1.0/watchface/api/hmUI/createWidget/>, section "Display levels of controls"):

| State (as the page names it) | Constant |
|---|---|
| normal_display | `hmUI.show_level.ONLY_NORMAL` |
| dropout (the rest screen, the AOD) | `hmUI.show_level.ONAL_AOD` |
| edit | `hmUI.show_level.ONLY_EDIT` |

- The AOD constant is spelled `ONAL_AOD` in the docs. It is not `ONLY_AOD`.
- The 1.0 docs list no `ALL` constant and no `ONLY_AOD`. The docs and official samples never use them. The Glass code falls back from `ONLY_AOD` to `ONAL_AOD`, which is harmless, but only `ONAL_AOD` is documented.
- Flags are combined with `|`. The docs example `hmUI.show_level.ONLY_NORMAL | hmUI.show_level.ONAL_AOD` is described as: "It means that it will only be displayed under the normal Watchface and rest screen, and will not be created under editable."
- **It must be set when the widget is created.** The page says: "Must be passed in at create time for this to work".
- `setProperty(hmUI.prop.VISIBLE, false)` hides a widget that already exists. The docs do not compare its cost with creating the widget only where needed.
- **How the face learns it is in AOD.** `hmSetting.getScreenType()` returns one of `APP`, `WATCHFACE`, `SETTINGS` or `AOD` (<https://docs.zepp.com/docs/1.0/reference/device-app-api/hmSetting/getScreenType/>). `hmSetting.screen_type.AOD` is described as "In the hibernation screen".
- **Official sample use.** In the official color-world and basketball samples, AOD-only widgets (the time digits, the background, the colon) use `show_level: hmUI.show_level.ONAL_AOD`, and normal-mode-only widgets use `ONLY_NORMAL`. Some widgets use both flags, for example the week widget in color-world. See `SAMPLES/color-world/watchface/square/index.js` and `SAMPLES/basketball/watchface/round/index.js`. Samples use a separate AOD-specific image for the time, not the normal one.
- **What the system does in AOD.** The 1.0 docs do not say how often the screen is refreshed (for example once a minute), or what the system draws. This is not verified. The AOD design rule that forbids a second hand (section 1) is the only hint.
- **Screen on, off and brightness.** `hmSetting.setBrightScreen(brightTime)` sets the "bright screen time" in seconds ([1, 2147483]). It is meant for apps that want the screen to stay on. The user's own watch settings already cover this. A face should not use it.
- **Always-on in newer docs.** The newer docs add API-based AOD settings (for example `getSettings().standby.style`, which marks "follow the current dial") that require version 3.0. They do not apply to the GTS 4 Mini on Zepp OS 1.0. Source: `https://github.com/zepp-health/zeppos-docs/blob/main/docs/reference/device-app-api/newAPI/display/getSettings.mdx`.

## 5. Other things on the face side

- **Data-bound widgets versus polling.** The 1.0 docs say that data updates are "done inside the firmware" and that listeners and timers are paused when the face is not shown (section 2). The data-bound widgets (for example `TEXT_IMG`, `IMG_LEVEL` and `IMG_POINTER` take a `type: hmUI.data_type.*`) take the value from the firmware, so no JS is needed to refresh them. For example, `IMG_POINTER` says "The data progress can be displayed by binding the data type `hmUI.data_type.*`" (`REPO1/watchface/api/hmUI/widget/IMG_POINTER.mdx`). The docs do not compare the cost of these with JS polling. That the data-bound way is cheaper is an inference.
- **Weather and heart rate widgets.** There is no battery warning on any of the 1.0 data pages I checked. The only element-priority guidance for AOD ("steps > date > weather > electricity > heart rate > others") is about AOD space, not power.
- **`lockscreen` and `photoscreen` flags.**
  - The 1.0 app.json reference (<https://docs.zepp.com/docs/1.0/watchface/app-json/>) lists `lockscreen` ("Lock screen(0:none)") and `photoscreen` ("Photo watchface (0: not supported)"). Both default to 0.
  - It also lists `main` (default 1) and `editable` (default 0).
  - Nothing in the docs ties any of these flags to battery or speed. Glass has `lockscreen: 0` and `editable: 0`.
- **Debug flag.** The app.json reference has `debug` (boolean, default `false`): "Mini Program debugging function ... `false` Default value. Turn off the debugging function." (`REPO1/reference/app-json.mdx`). Glass does not set it, so it is at the default. The docs do not say what the flag costs.
- **Developer-mode (QR preview) install versus a published install.** The CLI page (<https://docs.zepp.com/docs/1.0/guides/tools/cli/>) only says `zeus preview` shows a QR code to scan in the Zepp app with developer mode on. The docs do not compare power or speed with a published face. I found nothing, so this is not verified. Publishing needs review (<https://docs.zepp.com/docs/1.0/distribute/watchface/>), which takes "generally 1~5 working days", and no power check is mentioned there.
- **Logging.** The samples log with `console.log`/`logger.log` in `onInit`, `build` and `onDestroy`. There is no official advice on logging cost.

## Not verified / gaps

1. How the 1.0 TIME_POINTER second hand updates (per second or smooth), what it costs, and whether the `show_level` option is honoured by TIME_POINTER the same way as by other widgets. The docs list the warning about image count but nothing else.
2. How often the system refreshes the screen in AOD, and what happens to widgets with `show_level` ONLY_NORMAL when the screen goes to AOD (the docs say they "will not be created" there, but not how fast the switch is).
3. Whether the 10% lit-pixel figure is measured per element or for the whole screen. The specification text says both ("illuminated pixels do not exceed 10% of the screen" and "an element ... cannot exceed 10%"). The Glass AOD dial (white ticks, numbers) should be checked against it. I did not measure it.
4. Image storage and decoding: no docs on TGA conversion, colour depth, compression, RGB565, alpha, or what `zeus build` does to PNGs.
5. Memory limits and the cost of widget count, image count or image size on 1.0. `getPerformance` is documented only from API_LEVEL 4.0 (newer docs).
6. What the Watchface Maker "high power consumption Watchface" flag does, and whether Zeus code faces have an equivalent.
7. Anything that compares a developer-mode install with a published install.
8. The `ALL` and `ONLY_AOD` constants are not documented for 1.0. `ONAL_AOD` is the only AOD constant that appears in the docs and samples.
9. Wording risk: part of the live pages was read through an automatic page-to-text tool. I cross-checked the key quotes (AOD rules, show_level table, UI lifecycle table, TIME_POINTER warning, image format tip) against the files in the official docs repo, but a few small items (the HEART page and the getScreenType page quotes, and the hmUI.show_level text) rest on that tool's output plus the repo copy.
