/* Coloquio Parcial 1 - lógica con audios locales MP3 (edge-tts) */

(function () {
  "use strict";

  /* ============ ESTADO GLOBAL ============ */
  var PISTAS = window.PISTAS || [];
  var grid = document.getElementById("grid");
  var estadoTitulo = document.getElementById("estado-titulo");
  var estadoTiempo = document.getElementById("estado-tiempo");
  var barra = document.getElementById("progreso-barra");

  /* Controles flotantes */
  var floatBar = document.getElementById("floatBar");
  var opacitySlider = document.getElementById("opacitySlider");
  var compactToggle = document.getElementById("compactToggle");
  var enterFloatBtn = document.getElementById("enterFloat");
  var exitFloatBtn = document.getElementById("exitFloat");
  var header = document.getElementById("header");
  var footer = document.getElementById("footer");

  /* Configuración persistente */
  var CONFIG_KEY = "coloquio_float_cfg";
  var cfg = JSON.parse(localStorage.getItem(CONFIG_KEY) || "{}");
  var isFloating = cfg.floating || false;
  var isCompact = cfg.compact || false;
  var opacity = cfg.opacity !== undefined ? cfg.opacity : 95;

  /* Parámetros gestos */
  var UMBRAL_SWIPE = 55, UMBRAL_TAP = 10, MS_LARGO = 550, SALTO = 5;

  var actual = null;              // { pista, audioEl, started }
  var botones = {};
  var gesto = null, timerLargo = null, timerProgreso = null;

  /* Drag-to-scroll en grid */
  var gridDrag = null;

  /* ============ UTILIDADES ============ */
  function fmt(s) { if (!isFinite(s) || s < 0) s = 0; var m = Math.floor(s/60), sec = Math.floor(s%60); return m + ":" + (sec<10?"0":"")+sec; }
  function saveCfg() { localStorage.setItem(CONFIG_KEY, JSON.stringify({ floating: isFloating, compact: isCompact, opacity: opacity })); }
  function applyOpacity() { document.body.style.opacity = opacity/100; }
  function setFloating(on) {
    isFloating = on;
    document.body.classList.toggle("floating", on);
    floatBar.style.display = on ? "flex" : "none";
    enterFloatBtn.style.display = on ? "none" : "inline-flex";
    saveCfg();
    document.body.style.touchAction = on ? "none" : "auto";
  }
  function setCompact(on) {
    isCompact = on;
    document.body.classList.toggle("compact", on);
    compactToggle.setAttribute("aria-pressed", on ? "true" : "false");
    compactToggle.querySelector(".icon-full").style.display = on ? "none" : "block";
    compactToggle.querySelector(".icon-compact").style.display = on ? "block" : "none";
    saveCfg();
  }

  /* ============ INICIALIZACIÓN UI FLOTANTE ============ */
  function initFloatUI() {
    opacitySlider.value = opacity;
    applyOpacity();
    setFloating(isFloating);
    setCompact(isCompact);

    opacitySlider.addEventListener("input", function () {
      opacity = parseInt(this.value, 10);
      applyOpacity();
    });
    opacitySlider.addEventListener("change", saveCfg);

    enterFloatBtn.addEventListener("click", function () { setFloating(true); });
    exitFloatBtn.addEventListener("click", function () { setFloating(false); });
    compactToggle.addEventListener("click", function () { setCompact(!isCompact); });

    /* Drag-to-scroll en grid (pointer events) */
    grid.addEventListener("pointerdown", onGridDown);
    window.addEventListener("pointermove", onGridMove);
    window.addEventListener("pointerup", onGridUp);
    window.addEventListener("pointercancel", onGridCancel);
  }

  /* ---------- Drag-to-scroll grid ---------- */
  function onGridDown(e) {
    if (grid.scrollHeight <= grid.clientHeight) return;
    if (e.target.closest(".arg")) return;
    if (e.target.closest(".float-bar")) return;

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
    var dy = e.clientY - gridDrag.y;
    var dx = e.clientX - gridDrag.x;
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

  /* ============ AUDIO LOCAL (MP3) ============ */
  function crearAudio(pista) {
    var audio = new Audio(pista.archivo);
    audio.preload = "metadata";
    return audio;
  }

  function tocar(pista) {
    // Si ya está sonando este track
    if (actual && actual.pista.id === pista.id) {
      if (actual.audioEl.paused) {
        actual.audioEl.play().catch(function(e) { console.warn("Play error:", e); });
      } else {
        actual.audioEl.pause();
      }
      return;
    }

    // Nuevo track: detener anterior
    if (actual) {
      actual.audioEl.pause();
      actual.audioEl.currentTime = 0;
    }

    // Crear nuevo audio
    var audioEl = crearAudio(pista);
    actual = { pista: pista, audioEl: audioEl, started: false };

    audioEl.addEventListener("loadedmetadata", function () {
      actual.started = true;
      actualizarTiempo();
    });

    audioEl.addEventListener("timeupdate", actualizarTiempo);
    audioEl.addEventListener("ended", volverASeleccion);
    audioEl.addEventListener("pause", marcarActivo);
    audioEl.addEventListener("play", marcarActivo);
    audioEl.addEventListener("error", function (e) {
      console.error("Error audio:", e);
      estadoTitulo.textContent = "Error cargando audio " + pista.id;
    });

    audioEl.play().catch(function(e) { console.warn("Play error:", e); });
    marcarActivo();
  }

  function pausar() {
    if (actual && !actual.audioEl.paused) {
      actual.audioEl.pause();
    }
  }

  function reiniciarEnPausa(pista) {
    if (actual) {
      actual.audioEl.pause();
      actual.audioEl.currentTime = 0;
    }
    actual = { pista: pista };
    marcarActivo();
    if (navigator.vibrate) navigator.vibrate(15);
  }

  function volverASeleccion() {
    if (actual) {
      actual.audioEl.pause();
      actual.audioEl.currentTime = 0;
    }
    actual = null;
    marcarActivo();
  }

  function buscar(destino) {
    if (!actual || actual.audioEl.paused) return;
    var dur = actual.audioEl.duration || 0;
    actual.audioEl.currentTime = Math.max(0, Math.min(dur, destino));
  }

  function actualizarTiempo() {
    if (!actual || !actual.started) {
      estadoTiempo.textContent = "";
      barra.style.width = "0%";
      return;
    }
    var cur = actual.audioEl.currentTime || 0;
    var dur = actual.audioEl.duration || 0;
    if (isFinite(dur) && dur > 0) {
      estadoTiempo.textContent = fmt(cur) + " / " + fmt(dur);
      barra.style.width = Math.min(100, (cur/dur)*100) + "%";
    } else {
      estadoTiempo.textContent = fmt(cur);
      barra.style.width = "0%";
    }
  }

  function limpiarTimer() { if (timerLargo) { clearTimeout(timerLargo); timerLargo = null; } }
  function limpiarTimerProgreso() { if (timerProgreso) { clearInterval(timerProgreso); timerProgreso = null; } }

  /* ============ GESTOS EN BOTONES ============ */
  function onDown(e, pista) {
    if (gesto) return;
    if (e.pointerType==="mouse" && e.button!==0) return;
    gesto = { x:e.clientX, y:e.clientY, pista:pista, largo:false, movido:false, busco:false };
    limpiarTimer();
    timerLargo = setTimeout(function(){
      if(!gesto||gesto.movido)return;
      gesto.largo=true;
      reiniciarEnPausa(gesto.pista);
    }, MS_LARGO);
    try{e.currentTarget.setPointerCapture(e.pointerId);}catch(_){}
  }

  function onMove(e) {
    if(!gesto)return;
    var dx=e.clientX-gesto.x, dy=e.clientY-gesto.y;
    if(Math.abs(dx)>UMBRAL_TAP||Math.abs(dy)>UMBRAL_TAP){
      if(!gesto.largo){gesto.movido=true;limpiarTimer();}
    }
    if(gesto.largo||gesto.busco)return;
    var horizontal=Math.abs(dx)>UMBRAL_SWIPE&&Math.abs(dx)>Math.abs(dy)*1.4;
    if(!horizontal)return;
    gesto.movido=true; limpiarTimer();
    if(!actual || actual.audioEl.paused) return;
    gesto.busco=true;
    var cur = actual.audioEl.currentTime || 0;
    var destino = cur + (dx>0 ? SALTO : -SALTO);
    var dur = actual.audioEl.duration || destino;
    buscar(Math.max(0, Math.min(dur, destino)));
    actualizarTiempo();
  }

  function onUp() {
    if(!gesto)return;
    limpiarTimer();
    var g=gesto; gesto=null;
    if(g.largo||g.movido||g.busco)return;
    tocar(g.pista);
  }

  function onCancel() { limpiarTimer(); gesto=null; }

  /* ============ BOTONES ============ */
  function crearBoton(pista) {
    var b=document.createElement("button"); b.type="button"; b.className="arg"; b.setAttribute("aria-pressed","false"); b.setAttribute("aria-label", pista.id+". "+pista.titulo+". "+(pista.subtitulo||""));
    var num=document.createElement("span"); num.className="num"; num.textContent=pista.id;
    var titulo=document.createElement("span"); titulo.className="titulo"; titulo.textContent=pista.titulo;
    var sub=document.createElement("span"); sub.className="sub"; sub.textContent=pista.subtitulo||"";
    var marca=document.createElement("span"); marca.className="marca"; marca.setAttribute("aria-hidden","true");
    b.appendChild(num); b.appendChild(titulo); b.appendChild(sub); b.appendChild(marca);
    b.addEventListener("pointerdown",function(e){onDown(e,pista);}); b.addEventListener("pointermove",onMove); b.addEventListener("pointerup",onUp); b.addEventListener("pointercancel",onCancel); b.addEventListener("contextmenu",function(e){e.preventDefault();});
    return b;
  }

  function marcarActivo() {
    var enPausa = !actual || actual.audioEl.paused;
    for(var i=0;i<PISTAS.length;i++){
      var p=PISTAS[i], bt=botones[p.id];
      if(!bt)continue;
      var esActual = !!actual && actual.pista.id === p.id;
      bt.classList.toggle("activo", esActual);
      bt.classList.toggle("pausado", esActual && enPausa);
      bt.setAttribute("aria-pressed", esActual ? "true" : "false");
      var m=bt.querySelector(".marca");
      if(m) m.textContent = esActual ? (enPausa ? "Pausa" : "Sonando") : "";
    }
    if(actual){
      estadoTitulo.textContent = actual.pista.id + " · " + actual.pista.titulo;
      actualizarTiempo();
    } else {
      estadoTitulo.textContent = "Elegí una pregunta";
      estadoTiempo.textContent = "";
      barra.style.width = "0%";
    }
  }

  /* ============ INICIO ============ */
  function iniciar() {
    if(!PISTAS.length){ estadoTitulo.textContent="No se encontraron preguntas (falta tracks.js)"; return; }
    for(var i=0;i<PISTAS.length;i++){ var p=PISTAS[i], b=crearBoton(p); botones[p.id]=b; grid.appendChild(b); }
    initFloatUI();
    marcarActivo();
  }
  iniciar();
})();