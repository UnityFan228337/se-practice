// Room Availability Checker — client controller.
// Keeps the UI in sync and asks the Python server for every availability
// decision so the live preview and the final "Check" use the same rules.
(function () {
  const { config, rooms } = window.__CAMPUS__;
  const OPEN = config.open_min;
  const CLOSE = config.close_min;
  const SPAN = CLOSE - OPEN;
  const MAX = config.max_duration;

  const $ = (id) => document.getElementById(id);
  const startInput = $("startTime");
  const endInput = $("endTime");
  const startErr = $("startError");
  const endErr = $("endError");
  const campusTime = $("campusTime");
  const checkBtn = $("checkBtn");
  const resetBtn = $("resetBtn");
  const scheduleWrap = $("scheduleWrap");
  const emptyState = $("emptyState");
  const livePreview = $("livePreview");
  const livePreviewText = $("livePreviewText");
  const resultBanner = $("resultBanner");

  let selectedRoomId = null;
  let checked = false;

  const labelToMin = (l) => {
    if (!l) return null;
    const [h, m] = l.split(":").map(Number);
    if ([h, m].some((n) => Number.isNaN(n))) return null;
    return h * 60 + m;
  };
  const minToLabel = (min) => {
    const h = Math.floor(min / 60);
    const m = min % 60;
    return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
  };
  const pct = (min) => ((min - OPEN) / SPAN) * 100;

  function selectedRoom() {
    return rooms.find((r) => r.id === selectedRoomId) || null;
  }

  function overlaps(aS, aE, bS, bE) {
    return aS < bE && bS < aE;
  }

  // ---- Room cards -------------------------------------------------------
  document.querySelectorAll(".room-card").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (btn.disabled) return;
      selectRoom(btn.dataset.roomId);
    });
  });

  function selectRoom(id) {
    selectedRoomId = id;
    document.querySelectorAll(".room-card").forEach((btn) => {
      const room = rooms.find((r) => r.id === btn.dataset.roomId);
      const isActive = btn.dataset.roomId === id && !room.blocked;
      btn.classList.toggle("border-sky-500", isActive);
      btn.classList.toggle("bg-sky-50", isActive);
      btn.classList.toggle("ring-2", isActive);
      btn.classList.toggle("ring-sky-400/30", isActive);
      btn.classList.toggle("shadow-sm", isActive);
      btn.classList.toggle("border-slate-200", !isActive);
      btn.classList.toggle("bg-white", !isActive);
    });
    renderSchedule();
    refresh();
  }

  // ---- Schedule + timeline ---------------------------------------------
  function renderSchedule() {
    const room = selectedRoom();
    if (!room) {
      scheduleWrap.classList.add("hidden");
      emptyState.classList.remove("hidden");
      livePreview.classList.add("hidden");
      return;
    }
    emptyState.classList.add("hidden");
    scheduleWrap.classList.remove("hidden");
    livePreview.classList.remove("hidden");

    const bookings = room.bookings
      .map(
        (b) => `
        <div class="absolute top-0 bottom-0 bg-slate-400/60 border-x border-slate-500/40 flex items-center justify-center overflow-hidden"
             style="left:${pct(b.start)}%; width:${pct(b.end) - pct(b.start)}%;"
             title="${b.label} (${b.start_label}–${b.end_label})">
          <span class="text-[10px] text-white font-medium truncate px-1 hidden sm:block">${b.label}</span>
        </div>`
      )
      .join("");

    const now = labelToMin(campusTime.value) ?? 0;
    const nowMarker = `
      <div class="absolute top-0 bottom-0 w-px bg-amber-500 z-10" style="left:${pct(Math.min(Math.max(now, OPEN), CLOSE))}%;" title="Now">
        <div class="absolute -top-0 -translate-x-1/2 w-2 h-2 rounded-full bg-amber-500"></div>
      </div>`;

    const hourMarks = Array.from({ length: 25 }, (_, i) => i * 60)
      .filter((_, i) => i % 3 === 0)
      .map(
        (m) =>
          `<div class="absolute text-[10px] text-slate-400 -translate-x-1/2" style="left:${pct(m)}%;">${String(
            Math.floor(m / 60)
          ).padStart(2, "0")}:00</div>`
      )
      .join("");

    scheduleWrap.innerHTML = `
      <div class="border-t border-slate-100 pt-5 text-left">
        <div class="flex items-center justify-between mb-1">
          <h3 class="text-sm font-semibold text-slate-700">${room.name} — today</h3>
          <span class="text-xs text-slate-400">00:00 → 24:00</span>
        </div>
        <p class="text-xs text-slate-500 mb-2">
          Existing bookings shown in grey. Your candidate interval shows green (free) or red (conflict).
        </p>
        <div class="mt-4">
          <div class="relative h-12 rounded-lg bg-slate-100 border border-slate-200 overflow-hidden">
            ${bookings}${nowMarker}
            <div id="candidateBlock"></div>
          </div>
          <div class="relative h-5 mt-1">${hourMarks}</div>
        </div>
      </div>`;
    renderCandidateBlock();
  }

  function renderCandidateBlock() {
    const block = document.getElementById("candidateBlock");
    if (!block) return;
    const room = selectedRoom();
    const s = labelToMin(startInput.value);
    const e = labelToMin(endInput.value);
    if (!room || s === null || e === null || s >= e) {
      block.innerHTML = "";
      return;
    }
    const conflict = room.bookings.some((b) => overlaps(s, e, b.start, b.end)) || room.blocked;
    const color = conflict ? "bg-rose-400/50 border-rose-500" : "bg-emerald-400/50 border-emerald-500";
    block.innerHTML = `
      <div class="absolute top-0 bottom-0 ${color} border-2 border-dashed z-10"
           style="left:${pct(Math.max(s, OPEN))}%; width:${pct(e) - pct(Math.max(s, OPEN))}%;"></div>`;
  }

  // ---- Validation -------------------------------------------------------
  function validate() {
    const now = labelToMin(campusTime.value) ?? 0;
    const s = labelToMin(startInput.value);
    const e = labelToMin(endInput.value);

    let sErr = "";
    if (s === null) sErr = "Required";
    else if (s < OPEN || s >= CLOSE) sErr = `Must be ${minToLabel(OPEN)}–${minToLabel(CLOSE)}`;
    else if (s <= now) sErr = `Must be after now (${minToLabel(now)})`;

    let eErr = "";
    if (e === null) eErr = "Required";
    else if (e <= OPEN || e > CLOSE) eErr = `Must be ${minToLabel(OPEN)}–${minToLabel(CLOSE)}`;
    else if (s !== null && e <= s) eErr = "Must be after start";
    else if (s !== null && e - s > MAX) eErr = `Max ${MAX} min`;

    setError(startErr, sErr);
    setError(endErr, eErr);

    const ok = selectedRoomId !== null && sErr === "" && eErr === "";
    checkBtn.disabled = !ok;
    checkBtn.classList.toggle("bg-slate-200", !ok);
    checkBtn.classList.toggle("text-slate-400", !ok);
    checkBtn.classList.toggle("cursor-not-allowed", !ok);
    checkBtn.classList.toggle("bg-sky-600", ok);
    checkBtn.classList.toggle("text-white", ok);
    checkBtn.classList.toggle("hover:bg-sky-700", ok);
    checkBtn.classList.toggle("shadow-sm", ok);

    return { s, e, ok };
  }

  function setError(el, msg) {
    if (msg) {
      el.textContent = msg;
      el.classList.remove("hidden");
    } else {
      el.classList.add("hidden");
    }
  }

  // ---- Server preview ---------------------------------------------------
  async function fetchPreview() {
    const room = selectedRoom();
    if (!room) {
      livePreviewText.textContent = "—";
      return;
    }
    const params = new URLSearchParams({
      room_id: selectedRoomId,
      start: startInput.value,
      end: endInput.value,
      current: campusTime.value,
    });
    try {
      const res = await fetch(`/api/check?${params}`);
      const data = await res.json();
      const r = data.result;
      livePreviewText.textContent =
        r.reason_key === "no_room" ? "—" : r.available ? "Looks available" : r.reason;
    } catch (err) {
      livePreviewText.textContent = "Unable to reach server.";
    }
  }

  async function renderResult() {
    if (!checked) return;
    const params = new URLSearchParams({
      room_id: selectedRoomId,
      start: startInput.value,
      end: endInput.value,
      current: campusTime.value,
    });
    try {
      const res = await fetch(`/api/check?${params}`);
      const data = await res.json();
      const r = data.result;
      const ok = r.available;
      const icon = ok
        ? `<svg class="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`
        : `<svg class="w-5 h-5 text-rose-600 shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`;
      resultBanner.innerHTML = `
        <div class="rounded-xl border ${ok ? "border-emerald-300 bg-emerald-50" : "border-rose-300 bg-rose-50"} p-4 flex items-start gap-3 transition-all duration-300">
          ${icon}
          <div>
            <p class="font-semibold text-sm ${ok ? "text-emerald-800" : "text-rose-800"}">${ok ? "Available" : "Unavailable"}</p>
            <p class="text-sm mt-0.5 ${ok ? "text-emerald-700" : "text-rose-700"}">${r.reason}</p>
          </div>
        </div>`;
    } catch (err) {
      resultBanner.innerHTML = `<div class="rounded-xl border border-rose-300 bg-rose-50 p-4 text-sm text-rose-700">Unable to reach the server. Please try again.</div>`;
    }
  }

  // ---- Refresh on any input change -------------------------------------
  function refresh() {
    validate();
    renderCandidateBlock();
    fetchPreview();
    if (checked) renderResult();
  }

  [startInput, endInput, campusTime].forEach((el) =>
    el.addEventListener("input", refresh)
  );

  checkBtn.addEventListener("click", () => {
    const { ok } = validate();
    if (!ok) return;
    checked = true;
    renderResult();
  });

  resetBtn.addEventListener("click", () => {
    selectedRoomId = null;
    startInput.value = "09:00";
    endInput.value = "10:00";
    checked = false;
    selectRoom(null);
    validate();
    resultBanner.innerHTML = `
      <div class="rounded-xl border border-slate-200 bg-slate-50 p-4 flex items-center gap-3">
        <svg class="w-5 h-5 text-slate-400 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
        <p class="text-sm text-slate-500">Pick a room and enter a time range, then press <strong>Check Availability</strong>.</p>
      </div>`;
  });

  validate();
})();