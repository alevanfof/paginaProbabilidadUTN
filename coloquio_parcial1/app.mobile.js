/* ===== COLOQUIO PARCIAL 1 — LÓGICA MÓVIL (PWA) =====
   Sin Electron, sin ventana flotante, sin controles de opacidad/compacto.
   Mismos gestos: tap=play/pause, hold=reiniciar, swipe horizontal=seek ±5s.
   Drag-to-scroll en el grid.
*/

(function () {
  "use strict";

  /* ===== ESTADO ===== */
  const PISTAS = window.PISTAS || [];
  const grid = document.getElementById("grid");
  const estadoTitulo = document.getElementById("estado-titulo");
  const estadoTiempo = document.getElementById("estado-tiempo");
  const barra = document.getElementById("progreso-barra");
  const audioEl = document.getElementById("audio");

  /* Parámetros gestos */
  const UMBRAL_SWIPE = 55;
  const UMBRAL_TAP = 10;
  const MS_LARGO = 550;
  const SALTO = 5; // segundos

  let actual = null;              // { pista, started }
  const botones = {};
  let gesto = null, timerLargo = null;

  /* Drag-to-scroll en grid */
  let gridDrag = null;

  /* ===== UTILIDADES ===== */
  function fmt(s) {
    if (!isFinite(s) || s < 0) s = 0;
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return m + ":" + (sec < 10 ? "0" : "") + sec;
  }

  function marcarActivo() {
    const enPausa = !actual || audioEl.paused;
    for (const p of PISTAS) {
      const bt = botones[p.id];
      if (!bt) continue;
      const esActual = !!actual && actual.pista.id === p.id;
      bt.classList.toggle("activo", esActual);
      bt.classList.toggle("pausado", esActual && enPausa);
      bt.setAttribute("aria-pressed", esActual ? "true" : "false");
      const m = bt.querySelector(".marca");
      if (m) m.textContent = esActual ? (enPausa ? "Pausa" : "Sonando") : "";
    }
    if (actual) {
      estadoTitulo.textContent = actual.pista.id + " · " + actual.pista.titulo;
      actualizarTiempo();
    } else {
      estadoTitulo.textContent = "Elegí una pregunta";
      estadoTiempo.textContent = "";
      barra.style.width = "0%";
    }
  }

  function limpiarTimer() {
    if (timerLargo) { clearTimeout(timerLargo); timerLargo = null; }
  }

  /* ===== AUDIO LOCAL (MP3) ===== */
  function tocar(pista) {
    // Si ya está sonando este track
    if (actual && actual.pista.id === pista.id) {
      if (audioEl.paused) {
        audioEl.play().catch(e => console.warn("Play error:", e));
      } else {
        audioEl.pause();
      }
      return;
    }

    // Nuevo track: detener anterior
    if (actual) {
      audioEl.pause();
      audioEl.currentTime = 0;
    }

    audioEl.src = pista.archivo;
    audioEl.load();
    actual = { pista, started: false };

    audioEl.addEventListener("loadedmetadata", () => {
      actual.started = true;
      actualizarTiempo();
    }, { once: true });

    audioEl.addEventListener("timeupdate", actualizarTiempo);
    audioEl.addEventListener("ended", volverASeleccion);
    audioEl.addEventListener("pause", marcarActivo);
    audioEl.addEventListener("play", marcarActivo);
    audioEl.addEventListener("error", e => {
      console.error("Error audio:", e);
      estadoTitulo.textContent = "Error cargando audio " + pista.id;
    });

    audioEl.play().catch(e => console.warn("Play error:", e));
    marcarActivo();
  }

  function pausar() {
    if (actual && !audioEl.paused) audioEl.pause();
  }

  function reiniciarEnPausa(pista) {
    if (actual) {
      audioEl.pause();
      audioEl.currentTime = 0;
    }
    actual = { pista };
    marcarActivo();
    if (navigator.vibrate) navigator.vibrate(15);
  }

  function volverASeleccion() {
    if (actual) {
      audioEl.pause();
      audioEl.currentTime = 0;
    }
    actual = null;
    marcarActivo();
  }

  function buscar(destino) {
    if (!actual || audioEl.paused) return;
    const dur = audioEl.duration || 0;
    audioEl.currentTime = Math.max(0, Math.min(dur, destino));
  }

  function actualizarTiempo() {
    if (!actual || !actual.started) {
      estadoTiempo.textContent = "";
      barra.style.width = "0%";
      return;
    }
    const cur = audioEl.currentTime || 0;
    const dur = audioEl.duration || 0;
    if (isFinite(dur) && dur > 0) {
      estadoTiempo.textContent = fmt(cur) + " / " + fmt(dur);
      barra.style.width = Math.min(100, (cur / dur) * 100) + "%";
    } else {
      estadoTiempo.textContent = fmt(cur);
      barra.style.width = "0%";
    }
  }

  /* ===== GESTOS EN BOTONES ===== */
  function onDown(e, pista) {
    if (gesto) return;
    if (e.pointerType === "mouse" && e.button !== 0) return;
    gesto = { x: e.clientX, y: e.clientY, pista, largo: false, movido: false, busco: false };
    limpiarTimer();
    timerLargo = setTimeout(() => {
      if (!gesto || gesto.movido) return;
      gesto.largo = true;
      reiniciarEnPausa(gesto.pista);
    }, MS_LARGO);
    try { e.currentTarget.setPointerCapture(e.pointerId); } catch (_) {}
  }

  function onMove(e) {
    if (!gesto) return;
    const dx = e.clientX - gesto.x;
    const dy = e.clientY - gesto.y;
    if (Math.abs(dx) > UMBRAL_TAP || Math.abs(dy) > UMBRAL_TAP) {
      if (!gesto.largo) { gesto.movido = true; limpiarTimer(); }
    }
    if (gesto.largo || gesto.busco) return;
    const horizontal = Math.abs(dx) > UMBRAL_SWIPE && Math.abs(dx) > Math.abs(dy) * 1.4;
    if (!horizontal) return;
    gesto.movido = true;
    limpiarTimer();
    if (!actual || audioEl.paused) return;
    gesto.busco = true;
    const cur = audioEl.currentTime || 0;
    const destino = cur + (dx > 0 ? SALTO : -SALTO);
    const dur = audioEl.duration || destino;
    buscar(Math.max(0, Math.min(dur, destino)));
    actualizarTiempo();
  }

  function onUp() {
    if (!gesto) return;
    limpiarTimer();
    const g = gesto; gesto = null;
    if (g.largo || g.movido || g.busco) return;
    tocar(g.pista);
  }

  function onCancel() { limpiarTimer(); gesto = null; }

  /* ===== DRAG-TO-SCROLL EN GRID ===== */
  function onGridDown(e) {
    if (grid.scrollHeight <= grid.clientHeight) return;
    if (e.target.closest(".arg")) return;

    gridDrag = {
      x: e.clientX,
      y: e.clientY,
      scrollTop: grid.scrollTop,
      scrollLeft: grid.scrollLeft
    };
    grid.style.cursor = "grabbing";
    try { e.currentTarget.setPointerCapture(e.pointerId); } catch (_) {}
  }

  function onGridMove(e) {
    if (!gridDrag) return;
    const dy = e.clientY - gridDrag.y;
    const dx = e.clientX - gridDrag.x;
    grid.scrollTop = gridDrag.scrollTop - dy;
    grid.scrollLeft = gridDrag.scrollLeft - dx;
  }

  function onGridUp() {
    if (!gridDrag) return;
    gridDrag = null;
    grid.style.cursor = "grab";
  }

  function onGridCancel() {
    if (!gridDrag) return;
    gridDrag = null;
    grid.style.cursor = "grab";
  }

  /* ===== BOTONES ===== */
  function crearBoton(pista) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "arg";
    b.setAttribute("aria-pressed", "false");
    b.setAttribute("aria-label", pista.id + ". " + pista.titulo + ". " + (pista.subtitulo || ""));

    const num = document.createElement("span"); num.className = "num"; num.textContent = pista.id;
    const titulo = document.createElement("span"); titulo.className = "titulo"; titulo.textContent = pista.titulo;
    const sub = document.createElement("span"); sub.className = "sub"; sub.textContent = pista.subtitulo || "";
    const marca = document.createElement("span"); marca.className = "marca"; marca.setAttribute("aria-hidden", "true");

    b.appendChild(num); b.appendChild(titulo); b.appendChild(sub); b.appendChild(marca);
    b.addEventListener("pointerdown", e => onDown(e, pista));
    b.addEventListener("pointermove", onMove);
    b.addEventListener("pointerup", onUp);
    b.addEventListener("pointercancel", onCancel);
    b.addEventListener("contextmenu", e => e.preventDefault());
    return b;
  }

  /* ===== INICIO ===== */
  function iniciar() {
    if (!PISTAS.length) { estadoTitulo.textContent = "No se encontraron preguntas (falta tracks.js)"; return; }
    for (const p of PISTAS) {
      const b = crearBoton(p);
      botones[p.id] = b;
      grid.appendChild(b);
    }

    grid.addEventListener("pointerdown", onGridDown);
    window.addEventListener("pointermove", onGridMove);
    window.addEventListener("pointerup", onGridUp);
    window.addEventListener("pointercancel", onGridCancel);

    marcarActivo();
  }

  iniciar();
})();