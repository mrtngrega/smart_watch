// "Glass" watch face for the Amazfit GTS 4 Mini (336x384, Zepp OS 1.0).
// The images come from tools/make_assets.py; the sizes below must match what it prints.

const CX = 168
const CY = 192

// Normal screen vs always-on. The 1.0 docs spell the always-on level "ONAL_AOD". Always-on shows the same face
// minus the second hand (about 7% of the pixels lit; Zepp's guidance is 10% at most).
// The watch draws always-on shifted up and to the left by a fixed amount (seen on the real GTS 4 Mini,
// 2026-11-20: same direction every time, the whole face). The always-on copy is drawn this far down/right
// to cancel it, so the switch looks still. Positive = right / down.
const AOD_DX = 4
const AOD_DY = 4
const NORMAL = hmUI.show_level.ONLY_NORMAL
const AOD = hmUI.show_level.ONLY_AOD !== undefined ? hmUI.show_level.ONLY_AOD : hmUI.show_level.ONAL_AOD

const range = (n, f) => Array.from({ length: n }, (_, i) => f(i))
const TIME_DIGITS = range(10, (i) => `time_${i}.png`)
const DAY_DIGITS = range(10, (i) => `date_day_${i}.png`)
const WEEKDAYS = range(7, (i) => `date_wk_${i}.png`) // Monday first
const MONTHS = range(12, (i) => `date_mon_${i}.png`)

// Time "21:09": 4 digits of 27 px + a 14 px colon = 122 px, centred; digit images are 64 px tall.
const TIME_X = CX - 61
const TIME_Y = 232

// Date "THU · 19 NOV": weekday 51, gap 2, dot 14, gap 2, day 2x12, gap 7, month 47 = 147 px, centred.
const DATE_X = CX - 73
const DATE_Y = 293

function drawFace(level, ox, oy) {
  // Dial: ticks and numbers on plain black.
  hmUI.createWidget(hmUI.widget.IMG, { x: ox, y: oy, src: 'dial.png', show_level: level })

  hmUI.createWidget(hmUI.widget.IMG_TIME, {
    hour_zero: 1,
    hour_startX: TIME_X + ox,
    hour_startY: TIME_Y + oy,
    hour_array: TIME_DIGITS,
    hour_space: 0,
    hour_unit_sc: 'time_colon.png',
    hour_unit_tc: 'time_colon.png',
    hour_unit_en: 'time_colon.png',
    hour_align: hmUI.align.LEFT,
    minute_zero: 1,
    minute_follow: 1,
    minute_array: TIME_DIGITS,
    minute_space: 0,
    minute_align: hmUI.align.LEFT,
    show_level: level,
  })

  hmUI.createWidget(hmUI.widget.IMG_WEEK, {
    x: DATE_X + ox,
    y: DATE_Y + oy,
    week_en: WEEKDAYS,
    week_tc: WEEKDAYS,
    week_sc: WEEKDAYS,
    show_level: level,
  })
  hmUI.createWidget(hmUI.widget.IMG, { x: DATE_X + 53 + ox, y: DATE_Y + oy, src: 'date_dot.png', show_level: level })
  hmUI.createWidget(hmUI.widget.IMG_DATE, {
    day_startX: DATE_X + 69 + ox,
    day_startY: DATE_Y + oy,
    day_zero: 1,
    day_space: 0,
    day_align: hmUI.align.LEFT,
    day_en_array: DAY_DIGITS,
    day_sc_array: DAY_DIGITS,
    day_tc_array: DAY_DIGITS,
    month_startX: DATE_X + 100 + ox,
    month_startY: DATE_Y + oy,
    month_is_character: true,
    month_en_array: MONTHS,
    month_sc_array: MONTHS,
    month_tc_array: MONTHS,
    show_level: level,
  })

  // Hands, then the chrome cap over the centre.
  hmUI.createWidget(hmUI.widget.TIME_POINTER, {
    hour_centerX: CX + ox, hour_centerY: CY + oy, hour_posX: 8, hour_posY: 81, hour_path: 'hour.png',
    minute_centerX: CX + ox, minute_centerY: CY + oy, minute_posX: 6, minute_posY: 133, minute_path: 'minute.png',
    show_level: level,
  })
  hmUI.createWidget(hmUI.widget.IMG, { x: CX - 8 + ox, y: CY - 8 + oy, src: 'cap.png', show_level: level })
}

WatchFace({
  init_view() {
    drawFace(NORMAL, 0, 0)
    // The second hand goes on top of the cap, and only on the normal screen.
    hmUI.createWidget(hmUI.widget.TIME_POINTER, {
      second_centerX: CX, second_centerY: CY, second_posX: 2, second_posY: 142, second_path: 'second.png',
      show_level: NORMAL,
    })
    drawFace(AOD, AOD_DX, AOD_DY)
  },

  build() {
    this.init_view()
  },
})
