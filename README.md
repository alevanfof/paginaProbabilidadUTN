# Coloquio Parcial 2do Parcial — Probabilidad y Estadística (UTN)

Widget de estudio para el coloquio del **segundo parcial (Unidades 1, 2, 3 y 4)**.  
**46 preguntas** con respuestas teóricas puras, audio generado con **Edge TTS voz argentina** (`es-AR-ElenaNeural`).

---

## 📁 Estructura del repo (root = deploy Vercel)

```
paginaProbabilidadUTN/
├── index.html                    # Versión desktop (Electron)
├── index.mobile.html             # Versión móvil PWA (HTTPS)
├── app.js / app.mobile.js        # Lógica desktop / móvil
├── styles.css / styles.mobile.css
├── electron-main.js              # Ventana Electron nativa
├── package.json                  # Dependencias Electron
├── tracks.js                     # Manifiesto de audios (archivo: "audio/XX.mp3")
├── guiones.json                  # Textos fuente para TTS
├── generar_audio.py              # Generador de audios (edge-tts)
├── sw.js                         # Service Worker (offline PWA)
├── manifest.webmanifest          # PWA manifest
├── coloquio_parcial1_CELULAR.html  # HTML único offline (base64, 8 MB)
├── audio/                        # 46 archivos .mp3 (01.mp3 … 46.mp3)
├── icons/                        # Iconos PWA (SVG)
└── README.md
```

---

## 🚀 Cómo usar

### Desktop (Electron)
```bash
npm install
npm start
```
Ventana nativa, transparente, always-on-top, barra arrastrable completa, drag-to-scroll, gestos tap/hold/swipe.

### Móvil (PWA — requiere HTTPS)
1. **Deploy en Vercel**: conectar este repo (`alevanfof/paginaProbabilidadUTN`), Root Directory = `.` (raíz).
2. Abrir `https://tu-dominio.vercel.app/index.mobile.html` en Chrome Android.
3. Menú ⋮ → **"Instalar app"** / **"Añadir a pantalla de inicio"**.
4. Funciona offline (Service Worker cachea audios y assets).

### Móvil offline (archivo único, 8 MB)
- Copiar `coloquio_parcial1_CELULAR.html` al celular.
- Abrir con Chrome: `file:///storage/emulated/0/Download/coloquio_parcial1_CELULAR.html`
- **46 botones en grid 2 columnas**, audios embebidos en base64, sin red.

---

## 🎯 Contenido (46 tracks)

### Unidad 1 — Estadística descriptiva (1–17)
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

### Unidad 2 — Probabilidad (18–31)
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

### Unidad 3 — Distribuciones de probabilidad (32–38)
32. Variable aleatoria discreta: función de probabilidad, esperanza, varianza  
33. Distribución Binomial: n ensayos, p éxito, media np, varianza npq  
34. Distribución Hipergeométrica: población finita, sin reposición, N, K, n  
35. Distribución Poisson: eventos raros, lambda, media=varianza=lambda  
36. Aproximación Normal a Binomial y Poisson: corrección de continuidad  
37. Variable aleatoria continua: función de densidad, Normal estándar Z  

### Unidad 4 — Inferencia estadística (39–46)
38. Distribución muestral de la media: Teorema Central del Límite  
39. Estimación puntual vs intervalar: intervalo de confianza para media y proporción  
40. Nivel de confianza, margen de error, tamaño de muestra  
41. Contraste de hipótesis: nula, alternativa, estadístico, región crítica  
42. Errores Tipo I y II, nivel de significancia alpha, p-value  
43. Potencia del test, relación con n y tamaño de efecto  
44. Contraste para media (Z/t), proporción, varianza (chi-cuadrado)  
45. Contraste de dos medias (independientes/pareadas) y dos proporciones  

### TAI
46. TAI: población, muestra, variable (EPH Gran Rosario, aglomerado 4)

---

## 🔧 Regenerar audios (local)

```bash
# Requiere: pip install edge-tts
python generar_audio.py          # Genera audio/ + tracks.js + guiones.md
python generar_audio.py --texto  # Solo regenera tracks.js y guiones.md
```

- Voz: `es-AR-ElenaNeural` (argentina)
- Velocidad: `+0%`
- Reintentos automáticos ante rate-limit 429 de Microsoft

---

## 📦 Deploy en Vercel

1. https://vercel.com/new → Import `alevanfof/paginaProbabilidadUTN`
2. **Framework Preset:** Other
3. **Root Directory:** `.` (raíz del repo)
4. Build Command: (vacío)
5. Output Directory: (vacío)
6. Deploy

---

## 📝 Notas

- **Sin consejos ni guías** en los audios: solo definiciones, teoremas, clasificaciones y fórmulas.
- **R (lenguaje) no incluido** — no lo toman en el parcial.
- Audios generados con **Edge TTS** (Microsoft), calidad nativa, no Web Speech API.
- TAI corregido: **Gran Rosario (aglomerado 4)**, 330 hogares.