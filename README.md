# Coloquio Parcial 1 — Probabilidad y Estadística (UTN)

Widget de estudio para el coloquio del primer parcial (Unidades 1 y 2).  
32 preguntas con respuestas teóricas puras, audio generado con **Edge TTS voz argentina** (`es-AR-ElenaNeural`).

---

## 📁 Estructura del proyecto

```
coloquio_parcial1/
├── index.html                 # Versión desktop (Electron)
├── index.mobile.html          # Versión móvil PWA (HTTPS)
├── index.mobile.js            # Lógica PWA
├── styles.mobile.css          # Estilos móviles
├── app.js                     # Lógica desktop
├── styles.css                 # Estilos desktop
├── electron-main.js           # Ventana Electron nativa
├── package.json               # Dependencias Electron
├── tracks.js                  # Manifiesto de audios (archivo: "audio/XX.mp3")
├── guiones.json               # Textos fuente para TTS
├── generar_audio.py           # Generador de audios (edge-tts)
├── sw.js                      # Service Worker (offline PWA)
├── manifest.webmanifest       # PWA manifest
├── coloquio_parcial1_CELULAR.html  # HTML único offline (base64, 4 MB)
├── coloquio_parcial1_OFFLINE.html  # Versión anterior base64
├── audio/                     # 32 archivos .mp3 (01.mp3 … 32.mp3)
└── icons/                     # Iconos PWA (SVG)
```

---

## 🚀 Cómo usar

### Desktop (Electron)
```bash
cd coloquio_parcial1
npm install
npm start
```
Ventana nativa, transparente, always-on-top, barra arrastrable completa, drag-to-scroll, gestos tap/hold/swipe.

### Móvil (PWA — requiere HTTPS)
1. Desplegar en **Vercel / Netlify / GitHub Pages / Firebase** (carpeta `coloquio_parcial1/` como root).
2. Abrir `https://tu-dominio/index.mobile.html` en Chrome Android.
3. Menú ⋮ → **"Instalar app"** / **"Añadir a pantalla de inicio"**.
4. Funciona offline (Service Worker cachea audios y assets).

### Móvil offline (archivo único, 4 MB)
- Copiar `coloquio_parcial1_CELULAR.html` al celular.
- Abrir con Chrome: `file:///storage/emulated/0/Download/coloquio_parcial1_CELULAR.html`
- **32 botones en grid 2 columnas**, audios embebidos en base64, sin red.

---

## 🎯 Contenido (32 tracks)

**Unidad 1 — Estadística descriptiva (1–17)**
1. Población vs Muestra  
2. Muestra representativa  
3. Variable estadística  
4. Cualitativa vs Cuantitativa  
5. Código numérico no es cuantitativa  
6. Escalas de medición  
7. Frecuencias absoluta, relativa, acumulada  
8. Datos no agrupados vs agrupados  
9. Regla de Sturges  
10. Interpretar tabla de frecuencias  
11. Media vs Mediana vs Moda  
12. Asimetría y medidas de centro  
13. Rango, varianza, desvío, coeficiente de variación  
14. Cuartiles, percentiles, rango intercuartílico  
15. Medidas para datos agrupados  
16. Gráficos: barras vs histograma  
17. Boxplot y atípicos  

**Unidad 2 — Probabilidad (18–31)**
18. Combinatorio: tres preguntas clave  
19. Permutación, variación, combinación  
20. Experimento aleatorio y espacio muestral  
21. Operaciones entre sucesos  
22. Probabilidad clásica vs frecuencial  
23. Axiomas y reglas básicas  
24. Probabilidad condicional  
25. Regla del producto  
26. Sucesos independientes  
27. Probabilidad total  
28. Regla de Bayes  
29. Incompatibles vs Independientes  
30. Tabla doble entrada: simple, intersección, condicional  
31. Prior vs Posterior en Bayes  

**TAI**
32. TAI: población, muestra, variable (EPH Gran Córdoba)

---

## 🔧 Regenerar audios

```bash
cd coloquio_parcial1
# Requiere: pip install edge-tts
python generar_audio.py          # Genera audio/ + tracks.js + guiones.md
python generar_audio.py --texto  # Solo regenera tracks.js y guiones.md
```

- Voz: `es-AR-ElenaNeural` (argentina)
- Velocidad: `+0%`
- Reintentos automáticos ante rate-limit 429 de Microsoft

---

## 📦 Deploy en Vercel (recomendado)

```bash
# Desde la raíz del repo (paginaProbabilidadUTN/)
npx vercel
# Framework: Other
# Build command: (vacío)
# Output directory: coloquio_parcial1
```

O arrastrar la carpeta `coloquio_parcial1/` a https://app.netlify.com/drop

---

## 📍 Repo origen

```
https://github.com/alevanfof/paginaProbabilidadUTN.git
```

Subcarpeta: `coloquio_parcial1/` — aislada del resto del repo.

---

## 📝 Notas

- **No hay consejos ni guías de estudio** en los audios: solo definiciones, teoremas, clasificaciones y fórmulas.
- **R (lenguaje) no incluido** — no lo toman en el parcial.
- Audios generados con **Edge TTS** (Microsoft), calidad nativa, no Web Speech API.