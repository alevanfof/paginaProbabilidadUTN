#!/usr/bin/env python3
# Genera HTML móvil idéntico al patrón que funciona: defensa_oral_celular.html
# - Grid fijo 2 columnas
# - Botones circulares con min(38vw, 16.5vh, 150px)
# - Base64 inline en JSON
# - Layout centrado max-width 520px
import base64, json, os
from pathlib import Path

BASE = Path(__file__).resolve().parent
AUDIO = BASE / "audio"

with open(BASE / "guiones.json", encoding="utf-8") as f:
    guiones = json.load(f)

# Leer audios a base64 con prefijo data:
audio_b64 = {}
for p in guiones["pistas"]:
    apath = AUDIO / f"{p['id']}.mp3"
    if apath.exists():
        b64 = base64.b64encode(apath.read_bytes()).decode("ascii")
        audio_b64[p["id"]] = f"data:audio/mpeg;base64,{b64}"
        print(f"{p['id']}.mp3 -> {len(b64)} chars")
    else:
        print(f"FALTA {apath}")

# Construir PISTAS con campo archivo = data URL
pistas_con_audio = []
for p in guiones["pistas"]:
    pistas_con_audio.append({
        "id": p["id"],
        "titulo": p["titulo"],
        "subtitulo": p.get("subtitulo", ""),
        "archivo": audio_b64.get(p["id"], "")
    })

# CSS idéntico al patrón que funciona (adaptado a 32 botones = 16 filas x 2 cols)
css = """
/* Coloquio Parcial 1 - versión celular (patrón defensa_oral) */

:root {
  --bg: #0b1220;
  --bg-suave: #101a2b;
  --superficie: #151f31;
  --linea: #2b3b54;
  --texto: #e9eef6;
  --tenue: #8fa1b8;
  --acento: #0ea5e9;
  --acento-ink: #0b1220;
  --btn: min(38vw, 16.5vh, 150px);
  --gap: clamp(8px, 1.8vh, 16px);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body { height: 100%; }

body {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100%;
  min-height: 100dvh;
  padding: max(14px, env(safe-area-inset-top)) 16px max(12px, env(safe-area-inset-bottom));
  background: var(--bg);
  background-image:
    radial-gradient(120% 60% at 50% 0%, #16233a 0%, rgba(11, 18, 32, 0) 62%),
    linear-gradient(180deg, #0c1424 0%, #0a1019 100%);
  color: var(--texto);
  font-family: "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

/* cabecera */
.cabecera {
  width: 100%;
  max-width: 520px;
  text-align: center;
  margin-bottom: clamp(10px, 2.2vh, 22px);
}
.kicker {
  color: var(--acento);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.22em;
  text-transform: uppercase;
}
.cabecera h1 {
  margin-top: 4px;
  font-size: clamp(16px, 4.6vw, 20px);
  font-weight: 600;
  letter-spacing: 0.01em;
}
.bajada {
  margin-top: 5px;
  color: var(--tenue);
  font-size: clamp(11px, 3vw, 12.5px);
}

/* grilla: 2 columnas fijas */
.grid {
  display: grid;
  grid-template-columns: repeat(2, var(--btn));
  gap: var(--gap);
  justify-content: center;
  align-content: center;
  flex: 1 0 auto;
  width: 100%;
  max-width: 520px;
}

/* botón circular */
.arg {
  position: relative;
  width: var(--btn);
  height: var(--btn);
  border-radius: 50%;
  border: 1px solid var(--linea);
  background: var(--superficie);
  color: var(--texto);
  font-family: inherit;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: calc(var(--btn) * 0.018);
  padding: 14%;
  text-align: center;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  -webkit-touch-callout: none;
  user-select: none;
  touch-action: pan-y;
  outline: none;
}
.arg:focus-visible { box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.55); }

.arg .num {
  color: var(--tenue);
  font-size: calc(var(--btn) * 0.072);
  font-weight: 700;
  letter-spacing: 0.14em;
  line-height: 1;
}
.arg .titulo {
  font-size: calc(var(--btn) * 0.105);
  font-weight: 600;
  line-height: 1.12;
  letter-spacing: -0.005em;
}
.arg .sub {
  color: var(--tenue);
  font-size: calc(var(--btn) * 0.066);
  line-height: 1.15;
}
.arg .marca {
  min-height: calc(var(--btn) * 0.07);
  font-size: calc(var(--btn) * 0.055);
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  opacity: 0;
  line-height: 1;
}

/* estados */
.arg.activo {
  background: var(--acento);
  border-color: var(--acento);
  color: var(--acento-ink);
}
.arg.activo .num,
.arg.activo .sub { color: rgba(11, 18, 32, 0.66); }
.arg.activo .marca { opacity: 0.8; }

.arg.activo.pausado {
  background: var(--superficie);
  color: var(--acento);
  border-color: var(--acento);
}
.arg.activo.pausado .num,
.arg.activo.pausado .sub { color: var(--tenue); }
.arg.activo.pausado .marca { opacity: 1; }

/* pie */
.pie {
  width: 100%;
  max-width: 520px;
  margin-top: clamp(10px, 2vh, 20px);
}
.estado {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  min-height: 18px;
}
.estado-titulo {
  color: var(--texto);
  font-size: clamp(11px, 3vw, 12.5px);
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.estado-tiempo {
  color: var(--tenue);
  font-size: clamp(10px, 2.8vw, 11.5px);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}
.progreso {
  height: 2px;
  margin-top: 7px;
  background: var(--linea);
  border-radius: 2px;
  overflow: hidden;
}
.progreso-barra {
  width: 0;
  height: 100%;
  background: var(--acento);
}
.ayuda {
  margin-top: 9px;
  color: #6f8097;
  font-size: clamp(9px, 2.5vw, 10.5px);
  line-height: 1.45;
  text-align: center;
}

/* pantallas muy bajas */
@media (max-height: 640px) {
  .cabecera .bajada { display: none; }
  .ayuda { display: none; }
  .cabecera { margin-bottom: 8px; }
}

/* horizontal: 4 columnas */
@media (orientation: landscape) and (max-height: 560px) {
  :root { --btn: min(20vw, 30vh, 120px); }
  .grid { grid-template-columns: repeat(4, var(--btn)); }
  .cabecera { margin-bottom: 6px; }
  .cabecera .bajada { display: none; }
  .ayuda { display: none; }
  .pie { margin-top: 6px; }
}
"""

# JS idéntico al patrón que funciona
js = """
(function () {
  "use strict";

  var PISTAS = window.PISTAS || [];
  var audio = document.getElementById("audio");
  var grid = document.getElementById("grid");
  var estadoTitulo = document.getElementById("estado-titulo");
  var estadoTiempo = document.getElementById("estado-tiempo");
  var barra = document.getElementById("progreso-barra");

  var UMBRAL_SWIPE = 55;
  var UMBRAL_TAP = 10;
  var MS_LARGO = 550;
  var SALTO = 5;

  var actual = null;
  var botones = {};
  var gesto = null;
  var timerLargo = null;

  function fmt(segundos) {
    if (!isFinite(segundos) || segundos < 0) segundos = 0;
    var m = Math.floor(segundos / 60);
    var s = Math.floor(segundos % 60);
    return m + ":" + (s < 10 ? "0" : "") + s;
  }

  function fijarTiempo(t) {
    try { audio.currentTime = t; } catch (e) { /* metadata aun no cargada */ }
  }

  function limpiarTimer() {
    if (timerLargo) { clearTimeout(timerLargo); timerLargo = null; }
  }

  function actualizarTiempo() {
    if (!actual) {
      estadoTiempo.textContent = "";
      barra.style.width = "0%";
      return;
    }
    var dur = audio.duration;
    var cur = audio.currentTime || 0;
    if (isFinite(dur) && dur > 0) {
      estadoTiempo.textContent = fmt(cur) + " / " + fmt(dur);
      barra.style.width = Math.min(100, (cur / dur) * 100) + "%";
    } else {
      estadoTiempo.textContent = fmt(cur);
      barra.style.width = "0%";
    }
  }

  function marcarActivo() {
    var enPausa = audio.paused;
    for (var i = 0; i < PISTAS.length; i++) {
      var p = PISTAS[i];
      var b = botones[p.id];
      if (!b) continue;
      var esActual = !!actual && actual.id === p.id;
      b.classList.toggle("activo", esActual);
      b.classList.toggle("pausado", esActual && enPausa);
      b.setAttribute("aria-pressed", esActual ? "true" : "false");
      var marca = b.querySelector(".marca");
      if (marca) marca.textContent = esActual ? (enPausa ? "Pausa" : "Sonando") : "";
    }

    if (actual) {
      estadoTitulo.textContent = actual.id + " \u00b7 " + actual.titulo;
      actualizarTiempo();
    } else {
      estadoTitulo.textContent = "Eleg\u00ed una pregunta";
      estadoTiempo.textContent = "";
      barra.style.width = "0%";
    }
  }

  function cargar(pista) {
    if (actual && actual.id === pista.id) return;
    actual = pista;
    audio.src = pista.archivo;
    audio.preload = "auto";
    fijarTiempo(0);
    marcarActivo();
  }

  function reproducir() {
    if (!actual) return;
    var promesa = audio.play();
    if (promesa && typeof promesa.catch === "function") {
      promesa.catch(function (err) {
        if (err && err.name === "AbortError") return;
        console.warn("No se pudo reproducir:", err);
        estadoTitulo.textContent = "Toc\u00e1 de nuevo para reproducir";
      });
    }
  }

  function pausar() { audio.pause(); }

  function reiniciarEnPausa(pista) {
    cargar(pista);
    audio.pause();
    fijarTiempo(0);
    audio.addEventListener("loadedmetadata", function volverCero() {
      fijarTiempo(0);
      audio.removeEventListener("loadedmetadata", volverCero);
      actualizarTiempo();
    });
    marcarActivo();
    if (navigator.vibrate) navigator.vibrate(15);
  }

  function volverASeleccion() {
    audio.pause();
    fijarTiempo(0);
    actual = null;
    marcarActivo();
  }

  function tocar(pista) {
    if (actual && actual.id === pista.id) {
      if (audio.paused) reproducir();
      else pausar();
      return;
    }
    cargar(pista);
    reproducir();
  }

  function onDown(e, pista) {
    if (gesto) return;
    if (e.pointerType === "mouse" && e.button !== 0) return;

    gesto = {
      x: e.clientX,
      y: e.clientY,
      pista: pista,
      largo: false,
      movido: false,
      busco: false
    };

    limpiarTimer();
    timerLargo = setTimeout(function () {
      if (!gesto || gesto.movido) return;
      gesto.largo = true;
      reiniciarEnPausa(gesto.pista);
    }, MS_LARGO);

    try { e.currentTarget.setPointerCapture(e.pointerId); } catch (err) { }
  }

  function onMove(e) {
    if (!gesto) return;

    var dx = e.clientX - gesto.x;
    var dy = e.clientY - gesto.y;

    if (Math.abs(dx) > UMBRAL_TAP || Math.abs(dy) > UMBRAL_TAP) {
      if (!gesto.largo) {
        gesto.movido = true;
        limpiarTimer();
      }
    }

    if (gesto.largo || gesto.busco) return;

    var horizontal = Math.abs(dx) > UMBRAL_SWIPE && Math.abs(dx) > Math.abs(dy) * 1.4;
    if (!horizontal) return;

    gesto.movido = true;
    limpiarTimer();

    if (audio.paused || !actual || audio.ended) return;

    gesto.busco = true;
    var destino = audio.currentTime + (dx > 0 ? SALTO : -SALTO);
    var dur = isFinite(audio.duration) ? audio.duration : destino;
    fijarTiempo(Math.max(0, Math.min(dur, destino)));
    actualizarTiempo();
  }

  function onUp() {
    if (!gesto) return;
    limpiarTimer();
    var g = gesto;
    gesto = null;

    if (g.largo || g.movido || g.busco) return;
    tocar(g.pista);
  }

  function onCancel() {
    limpiarTimer();
    gesto = null;
  }

  function crearBoton(pista) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "arg";
    b.setAttribute("aria-pressed", "false");
    b.setAttribute("aria-label", pista.id + ". " + pista.titulo + ". " + (pista.subtitulo || ""));

    var num = document.createElement("span");
    num.className = "num";
    num.textContent = pista.id;

    var titulo = document.createElement("span");
    titulo.className = "titulo";
    titulo.textContent = pista.titulo;

    var sub = document.createElement("span");
    sub.className = "sub";
    sub.textContent = pista.subtitulo || "";

    var marca = document.createElement("span");
    marca.className = "marca";
    marca.setAttribute("aria-hidden", "true");

    b.appendChild(num);
    b.appendChild(titulo);
    b.appendChild(sub);
    b.appendChild(marca);

    b.addEventListener("pointerdown", function (e) { onDown(e, pista); });
    b.addEventListener("pointermove", onMove);
    b.addEventListener("pointerup", onUp);
    b.addEventListener("pointercancel", onCancel);
    b.addEventListener("contextmenu", function (e) { e.preventDefault(); });

    return b;
  }

  function iniciar() {
    if (!PISTAS.length) {
      estadoTitulo.textContent = "No se encontraron los audios";
      return;
    }
    for (var i = 0; i < PISTAS.length; i++) {
      var p = PISTAS[i];
      var b = crearBoton(p);
      botones[p.id] = b;
      grid.appendChild(b);
    }

    audio.addEventListener("play", marcarActivo);
    audio.addEventListener("pause", marcarActivo);
    audio.addEventListener("ended", volverASeleccion);
    audio.addEventListener("timeupdate", actualizarTiempo);
    audio.addEventListener("loadedmetadata", actualizarTiempo);
    audio.addEventListener("durationchange", actualizarTiempo);
    audio.addEventListener("seeked", actualizarTiempo);
    audio.addEventListener("error", function () {
      if (actual) estadoTitulo.textContent = "No se pudo cargar el audio " + actual.id;
    });

    marcarActivo();
  }

  iniciar();
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
    <span id="estado-titulo" class="estado-titulo">Eleg\u00ed una pregunta</span>
    <span id="estado-tiempo" class="estado-tiempo"></span>
  </div>
  <div class="progreso" aria-hidden="true"><div id="progreso-barra" class="progreso-barra"></div></div>
  <p class="ayuda">Tocar: reproducir / pausar \u00b7 Mantener: reiniciar \u00b7 Deslizar: \u00b15 s</p>
</footer>

<audio id="audio" preload="metadata" playsinline></audio>

<script>window.PISTAS = {json.dumps(pistas_con_audio, ensure_ascii=False)};</script>
<script>
{js}
</script>
</body>
</html>"""

out = BASE / "coloquio_parcial1_CELULAR.html"
out.write_text(html, encoding="utf-8")
size_mb = out.stat().st_size / 1024 / 1024
print(f"\nGenerado: {out.name} ({size_mb:.1f} MB)")