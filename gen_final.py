import asyncio
import edge_tts
import json
import re
from pathlib import Path

BASE = Path('.')
AUDIO = BASE / 'audio'
GUIONES = BASE / 'guiones.json'

with open(GUIONES, encoding='utf-8') as f:
    datos = json.load(f)

voz = 'es-AR-TomasNeural'
velocidad = '+0%'
pistas = datos['pistas']

def limpiar(texto):
    texto = texto.replace('\u2014', ', ').replace('\u2013', ', ')
    texto = texto.replace('\u201c', '').replace('\u201d', '')
    texto = texto.replace('\u2018', '').replace('\u2019', '')
    return re.sub(r'\s+', ' ', texto).strip()

async def gen_one(pista):
    destino = AUDIO / f'{pista["id"]}.mp3'
    if destino.exists() and destino.stat().st_size > 0:
        print(destino.name + ' ya existe')
        return
    texto = limpiar(pista['texto'])
    print('Generando ' + destino.name)
    com = edge_tts.Communicate(texto, voice=voz, rate=velocidad)
    await com.save(str(destino))
    print('OK ' + destino.name)

async def main():
    for p in pistas[25:]:
        await gen_one(p)
        print('Esperando 10s...')
        await asyncio.sleep(10)

asyncio.run(main())