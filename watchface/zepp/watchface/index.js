// "Glass" watch face for the Amazfit GTS 4 Mini (336x384, Zepp OS 1.0).
// The images come from tools/make_assets.py; the sizes below must match what it prints.

const CX = 168
const CY = 192

// Normal screen vs always-on. The 1.0 docs spell the always-on level "ONAL_AOD".
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

WatchFace({
  init_view() {
    // Dial: ticks, numbers and the faint centre glow (always-on gets a plain black one).
    hmUI.createWidget(hmUI.widget.IMG, { x: 0, y: 0, src: 'dial.png', show_level: NORMAL })
    hmUI.createWidget(hmUI.widget.IMG, { x: 0, y: 0, src: 'dial_aod.png', show_level: AOD })

    hmUI.createWidget(hmUI.widget.IMG_TIME, {
      hour_zero: 1,
      hour_startX: TIME_X,
      hour_startY: TIME_Y,
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
      show_level: NORMAL,
    })

    hmUI.createWidget(hmUI.widget.IMG_WEEK, {
      x: DATE_X,
      y: DATE_Y,
      week_en: WEEKDAYS,
      week_tc: WEEKDAYS,
      week_sc: WEEKDAYS,
      show_level: NORMAL,
    })
    hmUI.createWidget(hmUI.widget.IMG, { x: DATE_X + 53, y: DATE_Y, src: 'date_dot.png', show_level: NORMAL })
    hmUI.createWidget(hmUI.widget.IMG_DATE, {
      day_startX: DATE_X + 69,
      day_startY: DATE_Y,
      day_zero: 1,
      day_space: 0,
      day_align: hmUI.align.LEFT,
      day_en_array: DAY_DIGITS,
      day_sc_array: DAY_DIGITS,
      day_tc_array: DAY_DIGITS,
      month_startX: DATE_X + 100,
      month_startY: DATE_Y,
      month_is_character: true,
      month_en_array: MONTHS,
      month_sc_array: MONTHS,
      month_tc_array: MONTHS,
      show_level: NORMAL,
    })

    // Hands: glass on the normal screen, plain white and no second hand when always-on.
    hmUI.createWidget(hmUI.widget.TIME_POINTER, {
      hour_centerX: CX, hour_centerY: CY, hour_posX: 8, hour_posY: 81, hour_path: 'hour.png',
      minute_centerX: CX, minute_centerY: CY, minute_posX: 6, minute_posY: 133, minute_path: 'minute.png',
      second_centerX: CX, second_centerY: CY, second_posX: 2, second_posY: 142, second_path: 'second.png',
      show_level: NORMAL,
    })
    hmUI.createWidget(hmUI.widget.TIME_POINTER, {
      hour_centerX: CX, hour_centerY: CY, hour_posX: 8, hour_posY: 81, hour_path: 'hour_aod.png',
      minute_centerX: CX, minute_centerY: CY, minute_posX: 6, minute_posY: 133, minute_path: 'minute_aod.png',
      show_level: AOD,
    })

    // Glass cap over the centre.
    hmUI.createWidget(hmUI.widget.IMG, { x: CX - 8, y: CY - 8, src: 'cap.png', show_level: NORMAL | AOD })
  },

  build() {
    this.init_view()
  },
})
