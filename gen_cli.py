"""Genera los MP3 faltantes usando el CLI de edge-tts (subprocess),
evitando los problemas de la API async en este entorno."""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
AUDIO = BASE / "audio"
TMP = BASE / "_tmp_texto.txt"

with (BASE / "guiones.json").open(encoding="utf-8") as f:
    datos = json.load(f)

voz = datos.get("voz", "es-AR-ElenaNeural")
velocidad = datos.get("velocidad", "+0%")
pistas = datos["pistas"]


def limpiar(texto):
    texto = texto.replace("\u2014", ", ").replace("\u2013", ", ")
    texto = texto.replace("\u201c", "").replace("\u201d", "")
    texto = texto.replace("\u2018", "").replace("\u2019", "")
    return re.sub(r"\s+", " ", texto).strip()


def generar(pista):
    destino = AUDIO / f"{pista['id']}.mp3"
    if destino.exists() and destino.stat().st_size > 0:
        print(f"{destino.name} ya existe ({destino.stat().st_size} bytes), saltando")
        return True

    texto = limpiar(pista["texto"])
    TMP.write_text(texto, encoding="utf-8")

    cmd = [
        sys.executable, "-m", "edge_tts",
        "-f", str(TMP),
        "-v", voz,
        "--rate", velocidad,
        "--write-media", str(destino),
    ]

    for intento in range(1, 6):
        print(f"Generando {destino.name} (intento {intento})...", flush=True)
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if resultado.returncode == 0 and destino.exists() and destino.stat().st_size > 0:
            print(f"OK {destino.name} ({destino.stat().st_size} bytes)", flush=True)
            return True
        print(f"  fallo: {resultado.stderr.strip()[:200]}", flush=True)
        time.sleep(2 ** intento)

    print(f"FALLO {destino.name}", flush=True)
    return False


def main():
    fallback = False
    exitos = 0
    total = 0
    for pista in pistas:
        total += 1
        if generar(pista):
            exitos += 1
        else:
            fallback = True

    if TMP.exists():
        TMP.unlink()

    print(f"\nResultado: {exitos}/{total} audios OK")
    sizes = [(p.name, (AUDIO / p.name).stat().st_size) for p in [Path(f"{i:02d}.mp3") for i in range(1, 35)]]
    empty = [n for n, s in sizes if s == 0]
    print("Vacíos:", empty if empty else "ninguno")
    return 1 if fallback else 0


if __name__ == "__main__":
    raise SystemExit(main())
