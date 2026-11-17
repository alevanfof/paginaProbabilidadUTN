#!/usr/bin/env python3
# Versión 2: JSON en script type="application/json" + Blob URLs lazy + debug visible
import base64, json, os
from pathlib import Path

BASE = Path(__file__).resolve().parent
AUDIO = BASE / "audio"

with open(BASE / "guiones.json", encoding="utf-8") as f:
    guiones = json.load(f)

with open(BASE / "styles.mobile.css", encoding="utf-8") as f:
    css = f.read()

# Leer audios a base64 (solo para el JSON, no en JS ejecutable)
audio_b64 = {}
for p in guiones["pistas"]:
    apath = AUDIO / f"{p['id']}.mp3"
    if apath.exists():
        b64 = base64.b64encode(apath.read_bytes()).decode("ascii")
        audio_b64[p["id"]] = b64  # SIN prefijo data:
        print(f"{p['id']}.mp3 -> {len(b64)} chars")
    else:
        print(f"FALTA {apath}")

# JS que usa Blob URLs lazy
js = r"""
(function () {
  "use strict";
  // Parsear JSON desde script tag (no bloquea parser)
  var PISTAS = JSON.parse(document.getElementById('pistas-json').textContent);
  var AUDIO_B64 = JSON.parse(document.getElementById('audio-b64-json').textContent);
  var grid = document.getElementById("grid");
  var estadoTitulo = document.getElementById("estado-titulo");
  var estadoTiempo = document.getElementById("estado-tiempo");
  var barra = document.getElementById("progreso-barra");
  var audioEl = document.getElementById("audio");

  // Debug: mostrar que JS carga
  console.log("PISTAS:", PISTAS.length);
  estadoTitulo.textContent = "Cargando " + PISTAS.length + " preguntas...";

  var UMBRAL_SWIPE = 55, UMBRAL_TAP = 10, MS_LARGO = 550, SALTO = 5;
  var actual = null;
  var botones = {};
  var gesto = null, timerLargo = null;
  var gridDrag = null;
  var blobCache = {};

  function fmt(s) { if (!isFinite(s) || s < 0) s = 0; var m = Math.floor(s/60), sec = Math.floor(s%60); return m + ":" + (sec<10?"0":"")+sec; }

  function b64toBlob(b64, type) {
    var bin = atob(b64);
    var arr = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
    return new Blob([arr], {type: type});
  }

  function getAudioUrl(pistaId) {
    if (blobCache[pistaId]) return blobCache[pistaId];
    var b64 = AUDIO_B64[pistaId];
    if (!b64) return null;
    var blob = b64toBlob(b64, "audio/mpeg");
    var url = URL.createObjectURL(blob);
    blobCache[pistaId] = url;
    return url;
  }

  function marcarActivo() {
    var enPausa = !actual || audioEl.paused;
    for (var i=0;i<PISTAS.length;i++) {
      var p=PISTAS[i], bt=botones[p.id];
      if(!bt)continue;
      var esActual = !!actual && actual.pista.id === p.id;
      bt.classList.toggle("activo", esActual);
      bt.classList.toggle("pausado", esActual && enPausa);
      bt.setAttribute("aria-pressed", esActual ? "true" : "false");
      var m=bt.querySelector(".marca");
      if(m) m.textContent = esActual ? (enPausa ? "Pausa" : "Sonando") : "";
    }
    if(actual) {
      estadoTitulo.textContent = actual.pista.id + " \u00b7 " + actual.pista.titulo;
      actualizarTiempo();
    } else {
      estadoTitulo.textContent = "Eleg\u00ed una pregunta";
      estadoTiempo.textContent = "";
      barra.style.width = "0%";
    }
  }

  function limpiarTimer() { if (timerLargo) { clearTimeout(timerLargo); timerLargo = null; } }

  function tocar(pista) {
    if (actual && actual.pista.id === pista.id) {
      if (audioEl.paused) { audioEl.play().catch(function(e){console.warn("Play error:",e);}); }
      else { audioEl.pause(); }
      return;
    }
    if (actual) { audioEl.pause(); audioEl.currentTime = 0; }
    var url = getAudioUrl(pista.id);
    if (!url) { estadoTitulo.textContent = "Audio no encontrado: " + pista.id; return; }
    audioEl.src = url;
    audioEl.load();
    actual = { pista: pista, started: false };
    audioEl.addEventListener("loadedmetadata", function() { actual.started = true; actualizarTiempo(); }, {once:true});
    audioEl.addEventListener("timeupdate", actualizarTiempo);
    audioEl.addEventListener("ended", volverASeleccion);
    audioEl.addEventListener("pause", marcarActivo);
    audioEl.addEventListener("play", marcarActivo);
    audioEl.addEventListener("error", function(e) { console.error("Error audio:",e); estadoTitulo.textContent = "Error cargando audio " + pista.id; });
    audioEl.play().catch(function(e){console.warn("Play error:",e);});
    marcarActivo();
  }

  function reiniciarEnPausa(pista) {
    if (actual) { audioEl.pause(); audioEl.currentTime = 0; }
    actual = { pista: pista };
    marcarActivo();
    if (navigator.vibrate) navigator.vibrate(15);
  }

  function volverASeleccion() { if (actual) { audioEl.pause(); audioEl.currentTime = 0; } actual = null; marcarActivo(); }

  function buscar(destino) { if (!actual || audioEl.paused) return; var dur = audioEl.duration || 0; audioEl.currentTime = Math.max(0, Math.min(dur, destino)); }

  function actualizarTiempo() {
    if (!actual || !actual.started) { estadoTiempo.textContent = ""; barra.style.width = "0%"; return; }
    var cur = audioEl.currentTime || 0;
    var dur = audioEl.duration || 0;
    if (isFinite(dur) && dur > 0) { estadoTiempo.textContent = fmt(cur) + " / " + fmt(dur); barra.style.width = Math.min(100, (cur/dur)*100) + "%"; }
    else { estadoTiempo.textContent = fmt(cur); barra.style.width = "0%"; }
  }

  function onDown(e, pista) {
    if (gesto) return;
    if (e.pointerType==="mouse" && e.button!==0) return;
    gesto = { x:e.clientX, y:e.clientY, pista:pista, largo:false, movido:false, busco:false };
    limpiarTimer();
    timerLargo = setTimeout(function(){ if(!gesto||gesto.movido)return; gesto.largo=true; reiniciarEnPausa(gesto.pista); }, MS_LARGO);
    try{e.currentTarget.setPointerCapture(e.pointerId);}catch(_){}
  }

  function onMove(e) {
    if(!gesto)return;
    var dx=e.clientX-gesto.x, dy=e.clientY-gesto.y;
    if(Math.abs(dx)>UMBRAL_TAP||Math.abs(dy)>UMBRAL_TAP){ if(!gesto.largo){gesto.movido=true;limpiarTimer();} }
    if(gesto.largo||gesto.busco)return;
    var horizontal=Math.abs(dx)>UMBRAL_SWIPE&&Math.abs(dx)>Math.abs(dy)*1.4;
    if(!horizontal)return;
    gesto.movido=true; limpiarTimer();
    if(!actual || audioEl.paused) return;
    gesto.busco=true;
    var cur = audioEl.currentTime || 0;
    var destino = cur + (dx>0 ? SALTO : -SALTO);
    var dur = audioEl.duration || destino;
    buscar(Math.max(0, Math.min(dur, destino)));
    actualizarTiempo();
  }

  function onUp() { if(!gesto)return; limpiarTimer(); var g=gesto; gesto=null; if(g.largo||g.movido||g.busco)return; tocar(g.pista); }
  function onCancel() { limpiarTimer(); gesto=null; }

  function onGridDown(e) { if (grid.scrollHeight <= grid.clientHeight) return; if (e.target.closest(".arg")) return; gridDrag = { x:e.clientX, y:e.clientY, scrollTop:grid.scrollTop, scrollLeft:grid.scrollLeft }; grid.style.cursor="grabbing"; try{e.currentTarget.setPointerCapture(e.pointerId);}catch(_){} }
  function onGridMove(e) { if(!gridDrag)return; var dy=e.clientY-gridDrag.y, dx=e.clientX-gridDrag.x; grid.scrollTop=gridDrag.scrollTop-dy; grid.scrollLeft=gridDrag.scrollLeft-dx; }
  function onGridUp() { if(!gridDrag)return; gridDrag=null; grid.style.cursor="grab"; }
  function onGridCancel() { if(!gridDrag)return; gridDrag=null; grid.style.cursor="grab"; }

  function crearBoton(pista) {
    var b=document.createElement("button"); b.type="button"; b.className="arg"; b.setAttribute("aria-pressed","false"); b.setAttribute("aria-label", pista.id+". "+pista.titulo+". "+(pista.subtitulo||""));
    var num=document.createElement("span"); num.className="num"; num.textContent=pista.id;
    var titulo=document.createElement("span"); titulo.className="titulo"; titulo.textContent=pista.titulo;
    var sub=document.createElement("span"); sub.className="sub"; sub.textContent=pista.subtitulo||"";
    var marca=document.createElement("span"); marca.className="marca"; marca.setAttribute("aria-hidden","true");
    b.appendChild(num); b.appendChild(titulo); b.appendChild(sub); b.appendChild(marca);
    b.addEventListener("pointerdown",function(e){onDown(e,pista);});
    b.addEventListener("pointermove",onMove);
    b.addEventListener("pointerup",onUp);
    b.addEventListener("pointercancel",onCancel);
    b.addEventListener("contextmenu",function(e){e.preventDefault();});
    return b;
  }

  function iniciar() {
    if(!PISTAS.length){ estadoTitulo.textContent="No se encontraron preguntas"; return; }
    for(var i=0;i<PISTAS.length;i++){ var p=PISTAS[i], b=crearBoton(p); botones[p.id]=b; grid.appendChild(b); }
    grid.addEventListener("pointerdown",onGridDown);
    window.addEventListener("pointermove",onGridMove);
    window.addEventListener("pointerup",onGridUp);
    window.addEventListener("pointercancel",onGridCancel);
    marcarActivo();
  }

  // Iniciar cuando DOM listo
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciar);
  } else {
    iniciar();
  }
})();
"""

# Generar HTML
html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0ea5e9">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="mobile-web-app-capable" content="yes">
<title>Coloquio Parcial 1 \u2014 Probabilidad y Estad\u00edstica</title>
<style>
{css}
</style>
</head>
<body>

<header class="cabecera">
  <p class="kicker">Coloquio Parcial 1</p>
  <h1>Probabilidad y Estad\u00edstica \u00b7 Unidades 1 y 2</h1>
  <p class="bajada">Toc\u00e1 una pregunta para escuchar la respuesta clave.</p>
</header>

<main id="grid" class="grid" aria-label="Preguntas del coloquio"></main>

<footer class="pie">
  <div class="estado" aria-live="polite">
    <span id="estado-titulo" class="estado-titulo">Cargando...</span>
    <span id="estado-tiempo" class="estado-tiempo"></span>
  </div>
  <div class="progreso" aria-hidden="true"><div id="progreso-barra" class="progreso-barra"></div></div>
  <p class="ayuda">Tocar: reproducir / pausar \u00b7 Mantener: reiniciar \u00b7 Deslizar: \u00b15 s</p>
</footer>

<audio id="audio" preload="metadata" playsinline></audio>

<!-- JSON data (no se ejecuta, solo parse) -->
<script id="pistas-json" type="application/json">{json.dumps(guiones["pistas"], ensure_ascii=False)}</script>
<script id="audio-b64-json" type="application/json">{json.dumps(audio_b64, ensure_ascii=False)}</script>

<!-- JS ejecutable -->
<script>
{js}
</script>
</body>
</html>"""

out = BASE / "coloquio_parcial1_OFFLINE.html"
out.write_text(html, encoding="utf-8")
size_mb = out.stat().st_size / 1024 / 1024
print(f"\nGenerado: {out.name} ({size_mb:.1f} MB)")