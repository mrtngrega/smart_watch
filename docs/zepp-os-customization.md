# Zepp OS 1.0 on the GTS 4 Mini: how far can we strip it down?

Goal: keep only step counter, music (control phone music) and workout. Researched 2026-11-20 from primary sources only (docs.zepp.com, support.amazfit.com, the GTS 4 Mini user manual, github.com/zepp-health). Anything I could not confirm is marked "not verified".

Device facts: the GTS 4 Mini is Zepp OS **1.0**, square 336x384, deviceSource 246 (mainland China) and 247. Source: https://docs.zepp.com/docs/1.0/reference/related-resources/device-list/

## Answer in plain words

- **Steps on the face: yes, fully.** A 1.0 watch face can show the live step count (and the goal) with `TEXT_IMG` / `IMG_LEVEL` and `hmUI.data_type.STEP`, or with the STEP sensor. Easy, documented, works in a developer-mode install.
- **Tap zone to start a workout: yes, but only certain sports.** In 1.0 a face can have an `IMG_CLICK` area whose `type` is one of six workouts: outdoor running, walking, outdoor cycling, free training, pool swimming, open-water swimming. It does not open the generic workout list. Whether the tap runs the workout directly or opens its preparation page is not documented (not verified).
- **Tap zone to open music: not documented for 1.0.** The 1.0 `data_type` list has no music entry. The system-app IDs for Music and Workout (`SYSTEM_APP_MUSIC`, `SYSTEM_APP_SPORT`) exist only from API_LEVEL 3.0, and this watch is 1.0. So the face cannot reliably jump to the Music app. Music stays one gesture away: the Quick Access Apps screen, or a long-press of the side button remapped to Music.
- **A face cannot remove the system swipe screens or the app list.** Nothing in the 1.0 docs lets a watch face hide or disable shortcut cards, notifications, Control Center, Quick Access Apps or the app list. App JSON has no field for it, and a face cannot register gestures in the documented watch-face API (not verified in a face). Developers cannot replace system apps or change firmware.
- **What he must do himself (no code needed):**
  - On the watch, Settings > Preferences > Widget: choose which apps sit on the Quick Access (swipe-left) screen. Put Music, Workout and steps/Activity there.
  - On the watch, Settings > Preferences > Long Press Side Button: set it to Music or Workout.
  - In the Zepp app, Profile > Amazfit GTS 4 Mini > Shortcut Cards: remove the cards he doesn't want and sort the rest.
  - On the watch, Workout > Edit: trim the workout list to the few he uses.
  - In the Zepp app, delete any third-party apps via the App Store > Manage.
- **Cannot be done:** uninstalling or hiding the built-in apps (heart rate, sleep, PAI, alarm and so on) from the app list. I found no official GTS 4 Mini page that offers this (not verified either way; see section 2). The side button still opens the full app list.
- **Custom mini-app for music or workout on 1.0: no documented path.** A MUSIC sensor exists in the 1.0 API, but the doc says it controls playback "through the watch's speaker", not the phone (details in section 3). There is no workout-tracking API in 1.0. Workout extensions only exist from 3.5.
- **Publishing is not needed for the face.** Preview-QR / developer-mode installs run the same code as a published face (his own Glass install already works). The Zepp docs I read don't mention an install expiry (not verified).

## 1. Watch face (Zepp OS 1.0)

The 1.0 watch face docs are at https://docs.zepp.com/docs/1.0/watchface/watchface-quick-start/. The "Watchface API" sidebar there lists: IMG, TEXT_IMG, TEXT, ARC, FILL_RECT, STROKE_RECT, ARC_PROGRESS, IMG_PROGRESS, IMG_LEVEL, IMG_ANIM, IMG_POINTER, IMG_STATUS, IMG_TIME, TIME_POINTER, IMG_DATE, IMG_WEEK, DATE_POINTER, data_type, IMG_CLICK, BUTTON, GRADKIENT_POLYLINE, edit_watchface, plus hmUI create/set/get/deleteWidget, hmSetting, one hmSensor page (TIME), hmFS and timers. Source: https://docs.zepp.com/docs/1.0/watchface/api/hmUI/widget/IMG/ (sidebar). The sidebar shows no `hmApp` section for watch faces.

### (a) Step count

Two ways, both 1.0:

1. **Widget bound to data (no JS needed).** `data_type.STEP` = "Current Step Count" (max 5 digits) and `data_type.STEP_TARGET` = "Target number of steps". Source: https://docs.zepp.com/docs/1.0/watchface/api/hmUI/widget/data_type/

   `TEXT_IMG` example (verbatim from the page, with `type` selecting the data):

   ```javascript
   const dayText = hmUI.createWidget(hmUI.widget.TEXT_IMG, {
     x: 207,
     y: 340,
     type: hmUI.data_type.BATTERY,
     font_array: fontArray,
     h_space: 1,
     align_h: 16,
     text: '123'
   })
   ```

   For steps, replace `BATTERY` with `STEP`. `font_array` is the 0-9 image set; `type` is "Data type (see data_type)"; `text` overrides `type`. Source: https://docs.zepp.com/docs/1.0/watchface/api/hmUI/widget/TEXT_IMG/

   `IMG_LEVEL` (an image chosen from an array by level, e.g. a progress icon) takes `image_array`, `image_length` and `level`. The page example sets `level` by hand. Whether `type` binds it to data is not stated on that page (not verified). Source: https://docs.zepp.com/docs/1.0/watchface/api/hmUI/widget/IMG_LEVEL/

   First-party sample: the ColorWorld 1.0 face uses `config.dataType = hmUI.data_type.STEP` and passes `type: config.dataType` to its widgets. Source: https://github.com/zepp-health/zeppos-samples/blob/main/watchface/1.0/color-world/watchface/square/index.js

2. **Sensor in JS.** `hmSensor.createSensor(hmSensor.id.STEP)` gives `step.current` and `step.target`, and `step.addEventListener(hmSensor.event.CHANGE, cb)` fires when the value changes. Source: https://docs.zepp.com/docs/1.0/reference/device-app-api/hmSensor/sensorId/STEP/ (this page sits in the mini-app "Device App API"). The official 1.0 watch face sample "simple" does the same inside a face:

   ```javascript
   stepSensor = hmSensor.createSensor(hmSensor.id.STEP);
   stepSensor.addEventListener(hmSensor.event.CHANGE, function () {
       stepCount.setProperty(hmUI.prop.MORE, { text: `SC:${stepSensor.current}` });
   });
   ```

   Source: https://github.com/zepp-health/zeppos-samples/blob/main/watchface/1.0/simple/watchface/default-target/index.js

   The Step page doesn't say whether a permission is needed (not verified). The "simple" sample's `app.json` declares only `"permissions":["gps"]`, which suggests none is needed for STEP. Source: https://github.com/zepp-health/zeppos-samples/blob/main/watchface/1.0/simple/app.json

### (b) Tap zones that open a built-in app

- **Widget: `IMG_CLICK`.** The entire 1.0 page is one code example. The `type` property is marked "Must write. The action to jump." The page example:

  ```javascript
  hmUI.createWidget(hmUI.widget.IMG_CLICK, {
    x: 329, y: 337, w: 40, h: 23,
    src: rootPath + 'click.png',   // image shown when clicked
    type: hmUI.data_type.STRESS    // required: the action to jump to
  })
  ```

  Source: https://docs.zepp.com/docs/1.0/watchface/api/hmUI/widget/IMG_CLICK/ (the v2 docs page is the same, https://docs.zepp.com/docs/v2/watchface/api/hmUI/widget/IMG_CLICK/). The page has no parameter table and no `click_func`.
- **Which `type` values jump.** The 1.0 `data_type` page lists the "jump only" values: `OUTDOOR_RUNNING`, `WALKING` (the page spells it "Waking"), `OUTDOOR_CYCLING`, `FREE_TRAINING`, `POOL_SWIMMING`, `OPEN_WATER_SWIMMING`, each described as "can only be used with `IMG_CLICK` for jumping". Other values (STEP, HEART, STRESS, SLEEP, ALARM_CLOCK, COUNT_DOWN, STOP_WATCH and others) are data types. The example uses `STRESS`, so data types such as these evidently also act as jump targets. The page doesn't spell out which app each opens (not verified). Source: https://docs.zepp.com/docs/1.0/watchface/api/hmUI/widget/data_type/
- **Music.** There is no music value in the 1.0 `data_type` list, and none in the v2 list either (https://docs.zepp.com/docs/v2/watchface/api/hmUI/widget/data_type/). So a music tap zone is not documented for 1.0.
- **Steps page.** `STEP` is a data type, so `IMG_CLICK` with `type: hmUI.data_type.STEP` is the likely way to open the steps/Activity page, but the docs don't confirm the jump target (not verified).
- **`hmApp.startApp` / `hmApp.gotoPage`.** `startApp({ appid, url, native?, param })` takes a numeric app ID and a page path (example `appid: 1000001, url: 'pages/index2'`). The `native` field is listed with default `false` but "Not described". No system app IDs are listed. Source: https://docs.zepp.com/docs/1.0/reference/device-app-api/hmApp/startApp/. `gotoPage({ url, param })` only loads a page of the current app. Source: https://docs.zepp.com/docs/1.0/reference/device-app-api/hmApp/gotoPage/. Both live in the mini-app (Device App) API; the watch-face API sidebar doesn't show `hmApp`, so whether a face can call them is not verified.
- **System app IDs for Music and Workout exist only from API_LEVEL 3.0.** `launchApp` (the 2.0+ name of `startApp`) lists `SYSTEM_APP_MUSIC`, `SYSTEM_APP_SPORT`, `SYSTEM_APP_SPORT_HISTORY` and `SYSTEM_APP_SPORT_STATUS`, marked API_LEVEL 3.0, and its `native` flag ("whether to jump to the system App") is 3.0 as well. This is a v3+ page and does not apply to the GTS 4 Mini (1.0). Source: https://docs.zepp.com/docs/reference/device-app-api/newAPI/router/launchApp/. The 1.0 to 2.0 mapping `hmApp.startApp` to `launchApp` is in https://docs.huami.com/docs/guides/version-info/migration-guide/ (seen in search results only, not opened).
- **`BUTTON`** has `click_func` (a callback receiving the button instance), but the 1.0 page says nothing about jumping to apps. Source: https://docs.zepp.com/docs/1.0/watchface/api/hmUI/widget/BUTTON/

### (c) Showing music info or workout status on the face

- **Music info:** no watch-face `data_type` exists for it (see above). The mini-app API has a `MUSIC` sensor with `title`, `artist`, `isPlaying`, and a `CHANGE` event, but it is documented as "controls playback through the watch's speaker", and says nothing about the phone. The watch-face sidebar doesn't list it. Whether it works in a face or on the GTS 4 Mini is not verified. Source: https://docs.zepp.com/docs/1.0/reference/device-app-api/hmSensor/sensorId/MUSIC/
- **Workout status:** nothing in the 1.0 watch-face API shows a running workout. The six sport `data_type` values are explicitly jump-only. A face can show data like heart rate, calories and distance (data types BATTERY, STEP, CAL, HEART, DISTANCE, etc. in the `data_type` page), which are daily totals, not a live workout state.
- On the GTS 4 Mini itself, the watch controls phone music from its own Music app and the workout page, so there is a built-in route. See the manual: https://support.amazfit.com/en/amazfit_gts_4_mini/files/user-manual.pdf.pdf (workout page: "On the right side of the workout data page, you can control music playback on the mobile phone").

### (d) Can a face hide the system swipe screens?

- Not documented. The 1.0 `app.json` for a face has these `watchface` module fields: `path`, `main`, `editable`, `lockscreen`, `photoscreen`. None controls system gestures or the swipe screens. Source: https://docs.zepp.com/docs/1.0/reference/app-json/
- The user manual describes these screens as system features. Swipe down from the face = Control Center (battery, calendar, DND, flashlight, brightness, screen lock, theater mode, keep screen on, find phone, settings); swipe right = Shortcut Cards; swipe left = Quick Access Apps; the manual also says "swipe from left to right" opens the Notification Center. The manual contradicts itself on swipe-right, so the exact direction of Shortcut Cards vs Notifications is not verified. Press and hold the face = watch face selection and settings. Source: https://support.amazfit.com/en/amazfit_gts_4_mini/files/user-manual.pdf.pdf
- There is a gesture hook in the mini-app API: `hmApp.registerGestureEvent(cb)` where `true` "skips the default behavior" and `false` keeps it. The page's documented default is only for RIGHT (`hmApp.goBack`), and it doesn't say whether the hook applies to watch faces or can suppress the system edge swipes. Treat it as not available for faces (not verified). Source: https://docs.zepp.com/docs/1.0/reference/device-app-api/hmApp/gestureEvent/registerGestureEvent/

## 2. App list and watch menus on the GTS 4 Mini

All of this is from the official manual (https://support.amazfit.com/en/amazfit_gts_4_mini/files/user-manual.pdf.pdf, "Overseas Version", 23 pages) and the Amazfit support FAQ (https://support.amazfit.com/en/amazfit_gts_4_mini/user-guide) unless stated.

- **Open the app list:** "Wake up the device, press the side button" (the manual also says "on the watch face page"). Swipe up/down to browse, tap to open. Manual section "Device apps".
- **Hide or reorder apps in the app list:** I found no GTS 4 Mini page that describes it. The manual's app-list text covers only opening and browsing; the support index has FAQs on shortcut cards, workout list, apps install/delete, but none on app list order (https://support.amazfit.com/en/amazfit_gts_4_mini/user-guide). Not verified for this model.
  - Other Amazfit models document it: the Bip 3 manual says "Profile > Amazfit Bip 3 > App list management" changes the display order or hides apps. I saw this only in a search snippet of https://manual-cdn.zepp.com/uploads/doc/20220831/166194271382.pdf. Different model, so it may not exist on the GTS 4 Mini. The user can check the Zepp app under Profile > Amazfit GTS 4 Mini for an "App list management" entry (not verified).
- **Uninstall built-in apps:** the manual's "App installation and uninstallation" section covers apps from the app store only: Profile > Amazfit GTS 4 Mini > App settings > More > Go to store > App store > tap the installed app > Delete. The support FAQ gives Profile > Amazfit GTS 4 Mini > App Store > Manage > Delete App > Confirm (https://support.amazfit.com/en/amazfit_gts_4_mini/docs/TZlCdKKPCo6jRUx4Oahc3clVnye). That FAQ explicitly does not say whether pre-installed apps can be removed. So: built-in apps, removable or only hideable: not verified; the documented delete path is for store apps.
- **Quick Access Apps (swipe left):** on the watch, Settings > Preferences > Widget, swipe to see apps that can be set as quick access, remove one when the "Current apps" limit is reached and add the one you need. The limit number is not stated.
- **Long-press the side button** launches a chosen app: Settings > Preferences > Long Press Side Button.
- **Shortcut Cards:** on the watch, tap Settings at the bottom of the cards to add, delete and sort; in the Zepp app, Profile > My Devices > Amazfit GTS 4 Mini > Shortcut Cards ("Profile > Amazfit GTS 4 Mini > Shortcut Cards" in the manual). Source: https://support.amazfit.com/en/amazfit_gts_4_mini/docs/OYQ0dWJBYogFoIxmSVbcTvP3nfd. Whether every card can be removed (leaving the screen empty) is not stated (not verified).
- **Workout list:** App List > Workout > swipe to the end > Edit; move or delete entries; Add Workout to add. Source: https://support.amazfit.com/en/amazfit_gts_4_mini/docs/Tw5VdeQ6FophtfxHRkYcKSGXnph
- **Real-time data items during a workout** can also be edited (FAQ "How do I edit the real-time data items in Workout?", https://support.amazfit.com/en/amazfit_gts_4_mini/docs/WhgldYsbpops8VxDZCcc9Ao1nxb, listed in the support index; page itself not opened).
- **Music control:** the watch is a remote for the phone's music; needs the watch connected, Zepp app running in the background, and (as the FAQ says) notification-reading access on the phone for song info. Source: https://support.amazfit.com/en/amazfit_gts_4_mini/docs/OctDdriXUoXKSpxRYwpctn9Rn9g. The FAQ gives Android steps; whether iPhone needs anything extra is not verified.
- **Control Center** features are listed in the manual, but the manual doesn't say they can be turned off (not verified).
- **Notifications:** the Zepp app controls which phone apps notify (manual, "App alerts"; path not quoted here). A user who wants nothing extra on the watch can disable notification sources there (path not verified for iPhone).

## 3. Limits for developers on Zepp OS 1.0

What the docs show:

- **Two app types only:** `app.appType` is `app` (mini-program) or `watchface`. Source: https://docs.zepp.com/docs/1.0/reference/app-json/
- **Mini-program architecture:** a Device App (UI and sensors on the watch) plus an optional Side App (Settings App and Side Service, running on the phone inside the Zepp app). The Side Service has no UI and does network and data work; the Device App and Settings App can't talk directly. Source: https://docs.zepp.com/docs/1.0/guides/architecture/arc/. That page describes no background execution on the watch (not verified either way).
- **Module types in 1.0 `app.json`:** `page`, `shortcut` (jump to another mini-program or native app; mutually exclusive with `page`), `app-widget` (third-party Shortcut Card), `secondary-widget`, `watch-widget`, `watchface`, `app-side`, `setting`. All marked "minimum version v2" in the table, which refers to config version v2. Source: https://docs.zepp.com/docs/1.0/reference/app-json/. `shortcut.appLangType: 1` = native app, `path` = "native app's name", but the page gives no example and no list of native app names (not verified).
- **No replacing or hiding system apps.** The docs have no API or config for it (absence of evidence; the docs I read are silent). There is no firmware access.
- **Permissions:** an app must declare permissions in `app.json`; an undeclared permission makes the app "invalid". The page doesn't list the available permissions. Source: https://docs.zepp.com/docs/1.0/reference/app-json/
- **Sensors available in 1.0:** TIME, BATTERY, STEP, CALORIE, HEART, PAI, DISTANCE, STAND, WEATHER, FAT_BURRING (sic), SPO2, BODY_TEMP, STRESS, VIBRATE, WEAR, WORLD_CLOCK, SLEEP, MUSIC. There is no sport/workout sensor. Source: https://docs.zepp.com/docs/1.0/reference/device-app-api/hmSensor/sensorId/TIME/ (sidebar)
- **Music in 1.0:** the `MUSIC` sensor offers `title`, `artist`, `isPlaying`, `audInit()`, `audPlay()`, `audPause()`, `audPrev()`, `audNext()` and a CHANGE event. The doc's description is "Controls playback through the watch's speaker". It says some devices have no speaker and sensor creation fails there. It does not mention phone music. Whether it controls the phone on the GTS 4 Mini: not verified. Source: https://docs.zepp.com/docs/1.0/reference/device-app-api/hmSensor/sensorId/MUSIC/. The GTS 4 Mini speaker/mic situation: the 1.0 device list has no note on it (not verified).
- **Workout in 1.0:** no tracking API. The only sport-related support in 1.0 is jumping to a sport via `IMG_CLICK` (above). The official workout extension samples (running data assistant, pace master) are for Zepp OS 3.5, not 1.0. Source: https://github.com/zepp-health/zeppos-samples (structure: `application/1.0` to `4.2`, `watchface/1.0`, `workout-extensions/3.5`). Not applicable to the GTS 4 Mini.
- **Mini-app sample coverage for 1.0:** hello-world, calories, todo-list, fetch-api, plus four watch faces. No music or workout sample. Source: https://github.com/zepp-health/zeppos-samples
- **Mini-app launching from the face:** `hmApp.startApp` takes an app ID; mini-apps are launched from the app list after install, with the user still needing to find them. Not verified whether a store/dev-installed mini-app can be put on Quick Access (the manual says Quick Access takes "apps and features", Settings > Preferences > Widget).
- **hmApp utilities in 1.0:** `startApp`, `gotoPage`, `reloadPage`, `setLayerY`, `getLayerY`, `gotoHome`, `exit`, `goBack`, `setScreenKeep`, `packageInfo`, gesture, alarm, key and spin events. Source: https://docs.zepp.com/docs/1.0/reference/device-app-api/hmApp/startApp/ (sidebar). `alarm` (alarmNew) exists, which is the only documented scheduled-wake mechanism I saw (not opened, so not verified what it can do).

So for this user's goal: a mini-app cannot become a replacement system, and for music/workout the practical answer is to use the built-in Music and Workout apps and make them quick to reach.

## 4. Does anything need publishing?

- **Face with step count and the jump tap zones:** the code is the same either way. `zeus preview` compiles and shows a QR code that is scanned in the Zepp app's Developer Mode to install on the watch; Developer Mode is enabled via Profile > Bound Devices (bottom); the CLI must be logged in. Source: https://docs.zepp.com/docs/1.0/guides/tools/cli/. The page doesn't say anything about publishing, install expiry or feature differences (not verified). The user's own notes confirm Glass installed this way (project CLAUDE.md, 2026-11-19 entries).
- **Publishing** (for other people): register the app in the console, set the registered `appId` in `app.json`, upload a ZAB, submit for review (generally 1-5 working days). Source: https://docs.zepp.com/docs/1.0/distribute/. That page doesn't mention preview or developer mode.
- The account used by the CLI must be the same one the phone's Zepp app uses; this is already in the project notes, not re-verified here.
- The system-side settings in section 2 (Quick Access Apps, long-press side button, Shortcut Cards, workout list, delete apps) need no developer mode or publishing; they are normal user settings.

## Not verified / gaps

- Which app each `IMG_CLICK` data type jumps to on the GTS 4 Mini (only the six sport types are documented as jump-only), and whether a tap can start a workout directly.
- Whether a watch face may call `hmApp.startApp` or register gestures.
- Whether the MUSIC sensor works on the GTS 4 Mini and whether it controls phone playback.
- Whether any built-in app can be hidden or uninstalled on the GTS 4 Mini, and whether an "App list management" screen exists for it in the Zepp app.
- The maximum number of Quick Access Apps and whether Shortcut Cards can be emptied.
- Whether developer-mode installs expire.
- Whether Zepp's iPhone app differs from the Android steps in the music FAQ.
