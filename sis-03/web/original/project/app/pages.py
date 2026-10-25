"""Page rendering for the Room Availability Checker.

We render the index page in pure Python (no Jinja2 dependency). The page
is intentionally close in structure to the original React UI: header with
an editable "campus time", a room list, a checker panel with start/end
time inputs, a per-room timeline, a live-preview line, and a result
banner. The browser-side script in static/app.js drives the live preview
and the timeline.
"""
from __future__ import annotations

import html
import json
from typing import Any


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _j(value: Any) -> str:
    # For embedding into <script> JSON; safe because content is sample data.
    return json.dumps(value)


ICON_CHECK = (
    '<svg class="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>'
    '<polyline points="22 4 12 14.01 9 11.01"/></svg>'
)
ICON_X = (
    '<svg class="w-5 h-5 text-rose-600 shrink-0 mt-0.5" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round"><circle cx="12" cy="12" r="10"/>'
    '<line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>'
)


def _room_card(room: dict) -> str:
    if room["blocked"]:
        cls = ("border-slate-200 bg-slate-50 opacity-60 cursor-not-allowed")
        disabled = "disabled"
    else:
        cls = "border-slate-200 bg-white hover:border-sky-300 hover:shadow-sm"
        disabled = ""

    count = len(room["bookings"])
    plural = "" if count == 1 else "s"

    if room["blocked"]:
        badge = (
            '<div class="mt-2 inline-flex items-center gap-1 text-xs font-medium '
            'text-rose-600 bg-rose-50 px-2 py-0.5 rounded-full">'
            '<svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>'
            '<path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg> Blocked</div>'
        )
    else:
        badge = (
            f'<div class="mt-2 text-xs text-slate-400">{count} existing booking'
            f"{plural} · max {_esc(room['_max_duration'])} min</div>"
        )
        # _max_duration injected by caller via config; fallback below.

    return f"""
    <button data-room-id="{_esc(room['id'])}"
      class="room-card w-full text-left rounded-xl border p-4 transition-all duration-200 {cls}"
      {disabled}>
      <div class="flex items-start justify-between gap-2">
        <div class="min-w-0">
          <h3 class="font-semibold text-slate-800 text-sm truncate">{_esc(room['name'])}</h3>
          <div class="mt-1 flex flex-wrap items-center gap-x-3 gap-y-0.5 text-xs text-slate-500">
            <span class="inline-flex items-center gap-1">
              <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
              Floor {_esc(room['floor'])}
            </span>
            <span class="inline-flex items-center gap-1">
              <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M5 21V7l8-4v18"/><path d="M19 21V11l-6-4"/></svg>
              {_esc(room['building'])}
            </span>
          </div>
        </div>
        <span class="inline-flex items-center gap-1 text-xs font-medium text-slate-600 shrink-0">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          {_esc(room['capacity'])}
        </span>
      </div>
      {badge}
    </button>"""


def render_index(rooms: list[dict], config: dict, current_minutes: int, current_label: str) -> str:
    max_duration = config["max_duration"]
    rooms_html = "\n".join(
        _room_card({**r, "_max_duration": max_duration}) for r in rooms
    )

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Smart Campus Room Availability Checker</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <style>
      html {{ -webkit-text-size-adjust: 100%; }}
      body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif;
             -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }}
      .tabular-nums {{ font-variant-numeric: tabular-nums; }}
    </style>
  </head>
  <body class="min-h-screen bg-gradient-to-br from-slate-50 via-sky-50/40 to-slate-100">
    <header class="border-b border-slate-200/70 bg-white/80 backdrop-blur-sm sticky top-0 z-20">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500 to-cyan-600 flex items-center justify-center shadow-sm">
            <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 13V8a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h10" />
              <path d="m16 19 2 2 4-4" />
              <path d="M3 13h4l2 3h6l2-3h4" />
            </svg>
          </div>
          <div>
            <h1 class="text-lg font-bold text-slate-800 leading-tight">Room Availability Checker</h1>
            <p class="text-xs text-slate-500 hidden sm:block">Smart Campus · Northgate University</p>
          </div>
        </div>
        <div class="inline-flex items-center gap-2 text-xs text-slate-500 bg-slate-100 px-3 py-1.5 rounded-full">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" />
          </svg>
          <input id="campusTime" type="time" value="{_esc(current_label)}"
            class="bg-transparent text-xs font-medium tabular-nums text-slate-600 focus:outline-none focus:ring-2 focus:ring-sky-300/40 rounded px-1 -ml-1" />
          <span class="text-slate-400 hidden sm:inline">· campus time</span>
        </div>
      </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 sm:px-6 py-6 lg:py-8">
      <div class="grid lg:grid-cols-5 gap-6">
        <section class="lg:col-span-2">
          <div class="flex items-center justify-between mb-3">
            <h2 class="text-sm font-semibold text-slate-700">Rooms</h2>
            <span class="text-xs text-slate-400">{len(rooms)} total</span>
          </div>
          <div class="space-y-2.5">
            {rooms_html}
          </div>
        </section>

        <section class="lg:col-span-3">
          <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 sm:p-6">
            <h2 class="text-sm font-semibold text-slate-700 mb-4">Check a time interval</h2>

            <div class="grid sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium text-slate-600 mb-1">Start time</label>
                <input id="startTime" type="time" value="09:00"
                  class="w-full rounded-lg border px-3 py-2 text-sm text-slate-800 bg-white focus:outline-none focus:ring-2 transition-all border-slate-300 focus:ring-sky-300/40 focus:border-sky-400" />
                <p id="startError" class="mt-1 text-xs text-rose-600 hidden"></p>
              </div>
              <div>
                <label class="block text-xs font-medium text-slate-600 mb-1">End time</label>
                <input id="endTime" type="time" value="10:00"
                  class="w-full rounded-lg border px-3 py-2 text-sm text-slate-800 bg-white focus:outline-none focus:ring-2 transition-all border-slate-300 focus:ring-sky-300/40 focus:border-sky-400" />
                <p id="endError" class="mt-1 text-xs text-rose-600 hidden"></p>
              </div>
            </div>

            <div class="mt-4 flex flex-wrap gap-2 text-xs text-slate-400">
              <span class="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-slate-50 border border-slate-200">
                Range {_esc(config['open_label'])}–{_esc(config['close_label'])}
              </span>
              <span class="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-slate-50 border border-slate-200">
                Max {_esc(max_duration)} min
              </span>
              <span class="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-slate-50 border border-slate-200">
                Touching endpoints OK
              </span>
            </div>

            <div class="mt-5 flex gap-3">
              <button id="checkBtn"
                class="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all bg-slate-200 text-slate-400 cursor-not-allowed">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                Check Availability
              </button>
              <button id="resetBtn"
                class="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-100 transition-colors">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
                Reset
              </button>
            </div>

            <div id="scheduleWrap" class="mt-6 text-center py-10 border-2 border-dashed border-slate-200 rounded-xl hidden"></div>
            <div id="emptyState" class="mt-6 text-center py-10 border-2 border-dashed border-slate-200 rounded-xl">
              <svg class="w-8 h-8 text-slate-300 mx-auto mb-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 13V8a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h10"/><path d="m16 19 2 2 4-4"/><path d="M3 13h4l2 3h6l2-3h4"/></svg>
              <p class="text-sm text-slate-400">Select a room to view its schedule and timeline.</p>
            </div>

            <div id="livePreview" class="mt-4 text-xs text-slate-500 bg-slate-50 rounded-lg px-3 py-2 border border-slate-100 hidden">
              <span class="font-medium text-slate-600">Live preview:</span> <span id="livePreviewText">—</span>
            </div>
          </div>

          <div class="mt-4" id="resultBanner">
            <div class="rounded-xl border border-slate-200 bg-slate-50 p-4 flex items-center gap-3">
              <svg class="w-5 h-5 text-slate-400 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
              <p class="text-sm text-slate-500">Pick a room and enter a time range, then press <strong>Check Availability</strong>.</p>
            </div>
          </div>
        </section>
      </div>

      <footer class="mt-8 text-center text-xs text-slate-400">
        Fictional sample data for demonstration only · No real bookings are created or modified.
      </footer>
    </main>

    <script>
      window.__CAMPUS__ = {{ config: {_j(config)}, rooms: {_j(rooms)} }};
    </script>
    <script src="/static/app.js"></script>
  </body>
</html>"""