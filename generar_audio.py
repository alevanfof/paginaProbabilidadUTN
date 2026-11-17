#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_audio.py - Genera los audios del coloquio Parcial 1.

Lee `guiones.json`, sintetiza cada pregunta con edge-tts (voz es-AR)
y escribe:
    audio/01.mp3 ... audio/34.mp3
    tracks.js     (manifiesto embebido: funciona con file:// sin fetch)
    guiones.md    (texto completo, para leer o imprimir)

Uso:
    python generar_audio.py            # genera todo (salta los que ya existen)
    python generar_audio.py --texto    # solo regenera tracks.js y guiones.md
    python generar_audio.py --force    # regenera todos los audios
"""
from __future__ import annotations

import asyncio
import json
import re
import sys
from pathlib import Path

import edge_tts

BASE = Path(__file__).resolve().parent
GUIONES = BASE / "guiones.json"
AUDIO = BASE / "audio"


def cargar() -> dict:
    with GUIONES.open(encoding="utf-8") as f:
        return json.load(f)


def limpiar_para_tts(texto: str) -> str:
    """Deja el texto listo para sintetizar: sin markdown ni simbolos raros."""
    texto = texto.replace("\u2014", ", ")     # raya
    texto = texto.replace("\u2013", ", ")
    texto = texto.replace("\u201c", "").replace("\u201d", "")
    texto = texto.replace("\u2018", "").replace("\u2019", "")
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


async def sintetizar_con_reintentos(texto: str, salida: Path, voz: str, velocidad: str, max_intentos: int = 8) -> None:
    """Sintetiza con reintentos y backoff exponencial para evitar 429."""
    for intento in range(1, max_intentos + 1):
        try:
            comunicar = edge_tts.Communicate(texto, voice=voz, rate=velocidad)
            await comunicar.save(str(salida))
            return
        except Exception as e:
            if intento == max_intentos:
                raise
            # Backoff exponencial: 2s, 4s, 8s, 16s, 32s...
            espera = 2 ** intento
            print(f"    [Rate limit 429] Reintento {intento}/{max_intentos} en {espera}s...")
            await asyncio.sleep(espera)


async def generar_audios(datos: dict, force: bool = False) -> list[dict]:
    AUDIO.mkdir(exist_ok=True)
    voz = datos.get("voz", "es-AR-ElenaNeural")
    velocidad = datos.get("velocidad", "+0%")
    pistas = datos["pistas"]

    for i, pista in enumerate(pistas):
        destino = AUDIO / f"{pista['id']}.mp3"
        
        # Saltar si ya existe y no es --force
        if not force and destino.exists() and destino.stat().st_size > 0:
            print(f"  -> {destino.name}  [YA EXISTE, saltando]")
            continue
            
        texto = limpiar_para_tts(pista["texto"])
        print(f"  -> {destino.name}  ({len(texto.split())} palabras)")
        await sintetizar_con_reintentos(texto, destino, voz, velocidad)
        # Pausa adicional entre audios
        if i < len(pistas) - 1:
            await asyncio.sleep(2.0)
    return pistas


def escribir_tracks(pistas: list[dict]) -> Path:
    """Manifiesto JS embebido: evita fetch y CORS al abrir con file://."""
    limpio = [
        {
            "id": p["id"],
            "titulo": p["titulo"],
            "subtitulo": p.get("subtitulo", ""),
            "archivo": f"audio/{p['id']}.mp3",
        }
        for p in pistas
    ]
    contenido = (
        "/* Generado por generar_audio.py - no editar a mano */\n"
        "window.PISTAS = "
        + json.dumps(limpio, ensure_ascii=False, indent=2)
        + ";\n"
    )
    destino = BASE / "tracks.js"
    destino.write_text(contenido, encoding="utf-8")
    print(f"[OK] {destino.name}  ({len(limpio)} pistas)")
    return destino


def escribir_guiones(pistas: list[dict]) -> Path:
    lineas = [
        "# Guiones del coloquio Parcial 1",
        "",
        "> Documento generado automaticamente desde `guiones.json`.",
        "> Los audios se sintetizan con la voz `es-AR-ElenaNeural` (edge-tts).",
        "",
        "---",
        "",
    ]
    for p in pistas:
        lineas.append(f"## {p['id']} - {p['titulo']}")
        if p.get("subtitulo"):
            lineas.append(f"*{p['subtitulo']}*")
        lineas.append("")
        lineas.append(p["texto"])
        lineas.append("")
        lineas.append("---")
        lineas.append("")
    destino = BASE / "guiones.md"
    destino.write_text("\n".join(lineas), encoding="utf-8")
    print(f"[OK] {destino.name}")
    return destino


def main() -> int:
    force = "--force" in sys.argv
    solo_texto = "--texto" in sys.argv
    datos = cargar()
    pistas = datos["pistas"]
    print(f"Guiones: {len(pistas)} | voz: {datos.get('voz')} | ritmo: {datos.get('velocidad')}")

    if not solo_texto:
        print("Sintetizando audios...")
        asyncio.run(generar_audios(datos, force=force))

    escribir_tracks(pistas)
    escribir_guiones(pistas)

    if not solo_texto:
        print("\nArchivos de audio:")
        total = 0
        for p in pistas:
            f = AUDIO / f"{p['id']}.mp3"
            if f.exists():
                kb = f.stat().st_size / 1024
                total += f.stat().st_size
                print(f"  {f.name:10s} {kb:8.1f} KB")
            else:
                print(f"  {f.name:10s} FALTA")
        print(f"  TOTAL      {total / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())