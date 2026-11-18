# Guiones del coloquio Parcial 1

> Documento generado automaticamente desde `guiones.json`.
> Los audios se sintetizan con la voz `es-AR-ElenaNeural` (edge-tts).

---

## 01 - Población vs Muestra
*U1*

La población son todos los elementos que te interesan. La muestra es la parte que lográs observar. Cada elemento individual es una unidad elemental. Si medís a todos, eso es un censo.

---

## 02 - Muestra representativa
*U1*

Una muestra representativa refleja a la población. No alcanza con que sea grande: importa cómo se eligió. Si la selección fue sesgada, la muestra no sirve aunque tenga miles de casos.

---

## 03 - Variable estadística
*U1*

La variable es lo que cambia de un elemento a otro. En peso de los alumnos, cada alumno es la unidad elemental y el peso es la variable.

---

## 04 - Cualitativa vs Cuantitativa
*U1*

Cualitativa son categorías: nominal si no hay orden, ordinal si hay jerarquía. Cuantitativa son números: discreta si surge de contar, continua si surge de medir.

---

## 05 - Código numérico no es cuantitativa
*U1*

Si usás números como etiquetas: uno igual casa, dos igual depto, tres igual pieza, la variable sigue siendo cualitativa nominal. El código no la vuelve cuantitativa.

---

## 06 - Escalas de medición
*U1*

Nominal solo distingue categorías. Ordinal agrega orden. Intervalo permite restar pero el cero es arbitrario, como en Celsius. Razón tiene cero absoluto, así que podés decir el doble o la mitad, como en tiempo o ingreso.

---

## 07 - Frecuencias absoluta, relativa, acumulada
*U1*

La absoluta cuenta cuántas. La relativa es la proporción sobre el total. Las acumuladas van sumando las anteriores, pero solo tienen sentido si hay un orden.

---

## 08 - Datos no agrupados vs agrupados
*U1*

Pocos valores: no agrupados. Muchos valores o variable continua: se agrupan en intervalos. La marca de clase es el punto medio del intervalo y representa a todos los valores de esa clase. La amplitud es el ancho del intervalo.

---

## 09 - Regla de Sturges
*U1*

Sturges te da una cantidad razonable de clases para no quedarte ni muy corto ni muy largo. Es un criterio sistemático, no una verdad única.

---

## 10 - Interpretar tabla de frecuencias
*U1*

La frecuencia absoluta indica cuántas observaciones tienen ese valor. La relativa es la proporción del total. La acumulada suma las frecuencias hasta ese valor inclusive.

---

## 11 - Media vs Mediana vs Moda
*U1*

La media es el centro de gravedad, usa todos los valores pero se mueve con los extremos. La mediana es el valor del medio al ordenar, resiste outliers. La moda es lo que más se repite, y es la única que sirve para cualitativas.

---

## 12 - Asimetría y medidas de centro
*U1*

En simétricas las tres quedan cerca. En asimetría positiva, cola a la derecha, la media se va para arriba: media mayor que mediana mayor que moda. En negativa pasa lo inverso. En asimétricas la mediana describe mejor lo típico.

---

## 13 - Rango, varianza, desvío, coeficiente de variación
*U1*

El rango es solo max menos min. La varianza promedia los desvíos al cuadrado, en muestras se divide por n menos uno. El desvío es la raíz de la varianza y vuelve a las unidades originales. El coeficiente de variación es el desvío sobre la media en porcentaje: sirve para comparar dispersión relativa entre cosas con escalas distintas.

---

## 14 - Cuartiles, percentiles, rango intercuartílico
*U1*

El primer cuartil deja el 25 por ciento abajo, el segundo es la mediana, el tercero deja el 75. Los percentiles generalizan: el 90 deja el 90 por ciento abajo. El rango intercuartílico es Q3 menos Q1: mide la dispersión del 50 por ciento central y no se rompe con outliers.

---

## 15 - Medidas para datos agrupados
*U1*

Cuando ya tenés la tabla con intervalos, usás la marca de clase como valor representativo y ponderás por las frecuencias. La media es promedio ponderado. La mediana se busca en la clase donde la acumulada pasa la mitad y se interpola. Varianza y desvío se calculan igual pero con las marcas.

---

## 16 - Gráficos: barras vs histograma
*U1*

Barras para categóricas o discretas: las barras están separadas porque son categorías independientes. Histograma para continuas agrupadas: las barras se tocan porque los intervalos forman una escala continua. Circular para proporciones de pocas categorías.

---

## 17 - Boxplot y atípicos
*U1*

La caja va de Q1 a Q3, ahí está el 50 por ciento central. La mediana es la línea adentro. Los bigotes llegan hasta 1,5 veces el rango intercuartílico; lo que queda afuera son valores atípicos. Poner varios boxplots juntos permite comparar grupos.

---

## 18 - Combinatorio: tres preguntas clave
*U2*

Para elegir fórmula hay tres criterios: si importa el orden, si usás todos los elementos, si se permite repetir. Permutación: ordenás todo sin repetir. Variación simple: elegís algunos, el orden importa, no repetís. Variación con repetición: elegís algunos, el orden importa, podés repetir. Combinación: elegís algunos, el orden no importa.

---

## 19 - Permutación, variación, combinación
*U2*

Permutación es n factorial. Variación simple es n factorial sobre n menos k factorial. Variación con repetición es n a la k. Combinación es n factorial sobre k factorial por n menos k factorial.

---

## 20 - Experimento aleatorio y espacio muestral
*U2*

Determinista: mismas condiciones, mismo resultado. Aleatorio: puede dar resultados distintos. El espacio muestral es el conjunto de todos los resultados posibles. Un suceso es cualquier subconjunto. El imposible es el vacío, el seguro es todo el espacio.

---

## 21 - Operaciones entre sucesos
*U2*

Intersección: ocurren los dos a la vez. Unión: ocurre uno, el otro, o ambos. Complemento: no ocurre. Diferencia: ocurre el primero pero no el segundo. Incompatibles: no pueden ocurrir juntos, su intersección es vacía.

---

## 22 - Probabilidad clásica vs frecuencial
*U2*

Clásica o de Laplace: espacio finito y todos los resultados igualmente probables. Probabilidad es casos favorables sobre casos totales. Frecuencial: repetís muchas veces, la frecuencia relativa se estabiliza alrededor de la probabilidad.

---

## 23 - Axiomas y reglas básicas
*U2*

Tres axiomas: la probabilidad nunca es negativa. El espacio seguro tiene probabilidad uno. Si son incompatibles, la probabilidad de la unión es la suma. De ahí salen: probabilidad entre cero y uno, imposible es cero, complemento es uno menos la probabilidad. Para unión general se suma y se resta la intersección porque se contó dos veces.

---

## 24 - Probabilidad condicional
*U2*

Es la probabilidad de A sabiendo que pasó B. El universo se reduce a B. A dado B no es lo mismo que B dado A, porque el denominador cambia.

---

## 25 - Regla del producto
*U2*

La intersección es probabilidad de A por probabilidad de B dado A. Sin reposición: después de la primera extracción cambia la composición, hay dependencia. Con reposición: la composición vuelve a ser la misma, puede dar independencia.

---

## 26 - Sucesos independientes
*U2*

Son independientes si saber que pasó uno no cambia la probabilidad del otro. En la práctica: si la intersección es igual al producto de las marginales, son independientes.

---

## 27 - Probabilidad total
*U2*

El mismo suceso puede pasar por varias causas excluyentes que cubren todo el espacio. La probabilidad total suma la probabilidad de cada causa por la probabilidad del suceso dentro de esa causa.

---

## 28 - Regla de Bayes
*U2*

Bayes invierte la condicional. Tenés varias causas posibles y la probabilidad de ver un resultado bajo cada una. Observás el resultado y querés saber cuál causa es más plausible. La posterior es la prior por la verosimilitud, dividido la probabilidad total.

---

## 29 - Incompatibles vs Independientes
*U2*

Incompatibles: no pasan juntos, intersección vacía, suma de probabilidades. Independientes: uno no cambia la chance del otro, producto de probabilidades. Son cosas distintas: dos sucesos pueden ser incompatibles pero no independientes, o viceversa.

---

## 30 - Tabla doble entrada: simple, intersección, condicional
*U2*

Probabilidad simple: celda sobre total. Intersección: fila y columna sobre total. Condicional: celda sobre total de la fila o columna que te condiciona. El universo se reduce al margen que te dan.

---

## 31 - Prior vs Posterior en Bayes
*U2*

La prior es lo que creés antes de ver la evidencia. La posterior es lo que creés después de verla. Bayes actualiza tus creencias con la información nueva.

---

## 32 - TAI: población, muestra, variable
*U1*

En el TAI de la EPH Gran Rosario: la población son los hogares del aglomerado 4. La muestra son los 330 hogares del archivo. Cada hogar es la unidad elemental. La variable depende del análisis: ingreso total familiar (ITF), tipo de vivienda (IV1), régimen de tenencia (II7), lo que estés estudiando.

---

## 33 - Variable aleatoria discreta: función de probabilidad, esperanza, varianza
*U3*

Una variable aleatoria discreta asigna un número a cada resultado del espacio muestral. Su función de probabilidad f(x) da la probabilidad de cada valor posible: suma f(x) = 1. La esperanza E(X) es el promedio ponderado: suma x·f(x). La varianza Var(X) mide dispersión: E(X²) - [E(X)]². El desvío es la raíz de la varianza.

---

## 34 - Distribución Binomial: n ensayos, p éxito, media np, varianza npq
*U3*

Binomial modela n ensayos independientes e idénticos con dos resultados: éxito (probabilidad p) y fracaso (q=1-p). La variable X = número de éxitos en n ensayos. f(x) = C(n,x)·pˣ·qⁿ⁻ˣ para x=0,1,...,n. Media = n·p. Varianza = n·p·q. Desvío = √(n·p·q). Se usa cuando: ensayos fijos, independientes, dos resultados, p constante.

---

## 35 - Distribución Hipergeométrica: población finita, sin reposición
*U3*

Corresponde hipergeométrica cuando la muestra se extrae de una población finita y la composición cambia en cada selección, o sea, sin reposición. En el TAI: 330 hogares forman la población, 70 son inquilinos, se eligen 15 sin reposición. La variable X es la cantidad de inquilinos seleccionados. La fórmula usa combinatorios: f(x) = C(K,x)·C(N-K,n-x) / C(N,n). Media = n·K/N. El factor (N-n)/(N-1) corrige por población finita. Se usa siempre que muestrees sin reposición de una población finita.

---

## 36 - Distribución Poisson: conteos en el tiempo, tasa constante
*U3*

Uso Poisson para conteos de ocurrencias en un intervalo con tasa promedio constante e independencia. En el TAI: el servidor del INDEC recibe 12 formularios por hora en promedio. X cuenta llegadas en el intervalo. La clave es ajustar lambda al intervalo: 15 minutos → λ=3; 30 minutos → λ=6; 45 minutos → λ=9. Fórmula: f(x) = e⁻ˡ·λˣ / x!. Media = λ, varianza = λ, desvío = √λ. Se usa para conteos en tiempo/espacio con tasa constante.

---

## 37 - Aproximación Normal a Binomial y Poisson: corrección de continuidad
*U3*

Binomial se aproxima a Normal si n·p > 5 y n·q > 5. Media = np, desvío = √(npq). Poisson se aproxima a Normal si λ > 10. Media = λ, desvío = √λ. Corrección de continuidad: para P(X ≤ k) usar P(X < k+0.5); P(X ≥ k) usar P(X > k-0.5); P(X = k) usar P(k-0.5 < X < k+0.5). Estandarizar Z = (x - μ) / σ y usar tabla Normal estándar. En síntesis: la Normal aproxima a Binomial y Poisson cuando los parámetros son grandes.

---

## 38 - Variable aleatoria continua: Normal, áreas bajo la curva
*U3*

La Normal representa las áreas de una variable continua: la probabilidad es el área bajo la curva de densidad. Variable continua toma infinitos valores; f(x) ≥ 0 y área total = 1. P(a < X < b) = área bajo la curva. Normal estándar Z ~ N(0,1): media 0, desvío 1. Cualquier X ~ N(μ,σ) se estandariza: Z = (X - μ) / σ. Tabla Z da P(Z < z). En síntesis: hipergeométrica = sin reposición; Normal = áreas continuo; Poisson = conteos tasa constante.

---

## 39 - Distribución muestral de la media: Teorema Central del Límite
*U4*

La distribución muestral de la media describe cómo varía x̄ entre muestras. Teorema Central del Límite: para n ≥ 30, x̄ ~ N(μ, σ/√n) aproximadamente, sin importar la forma de la población. Si la población es Normal, x̄ es exactamente Normal para cualquier n. Error estándar = σ/√n (si σ conocido) o s/√n (si σ desconocido).

---

## 40 - Estimación puntual vs intervalar: intervalo de confianza para media y proporción
*U4*

Estimación puntual: un solo valor (x̄ para μ, p̂ para p). Estimación intervalar: rango con nivel de confianza 1-α. Intervalo para media (σ conocido): x̄ ± Zα/2 · σ/√n. Intervalo para media (σ desconocido, n<30): x̄ ± tα/2,n-1 · s/√n. Intervalo para proporción: p̂ ± Zα/2 · √(p̂q̂/n). Nivel de confianza típico: 90%, 95%, 99%.

---

## 41 - Nivel de confianza, margen de error, tamaño de muestra
*U4*

Nivel de confianza 1-α: probabilidad de que el intervalo cubra el parámetro. Margen de error E = valor crítico · error estándar. Tamaño de muestra para media: n = (Zα/2 · σ / E)² (redondear al entero superior). Para proporción: n = (Zα/2)² · p̂q̂ / E² (usar p̂=0.5 si no hay info previa, maximiza n).

---

## 42 - Contraste de hipótesis: nula, alternativa, estadístico, región crítica
*U4*

Hipótesis nula H₀: afirma igualdad o status quo (μ = μ₀). Hipótesis alternativa H₁: lo que se quiere probar (μ ≠ μ₀ bilateral; μ > μ₀ o μ < μ₀ unilateral). Estadístico de prueba: Z = (x̄ - μ₀) / (σ/√n) o t = (x̄ - μ₀) / (s/√n). Región crítica: valores del estadístico que llevan a rechazar H₀. Valor crítico Zα/2 o tα/2 separa región de aceptación y rechazo.

---

## 43 - Errores Tipo I y II, nivel de significancia alpha, p-value
*U4*

Error Tipo I (α): rechazar H₀ siendo verdadera. Nivel de significancia α = P(Error Tipo I). Error Tipo II (β): no rechazar H₀ siendo falsa. Potencia = 1-β = P(rechazar H₀ | H₀ falsa). p-value: probabilidad de obtener un resultado tan extremo o más, asumiendo H₀ verdadera. Decisión: si p-value < α → rechazar H₀; si p-value ≥ α → no rechazar H₀.

---

## 44 - Potencia del test, relación con n y tamaño de efecto
*U4*

Potencia = 1-β aumenta con: n más grande, α más grande, tamaño de efecto mayor (diferencia real mayor), σ menor. Tamaño de efecto Cohen's d = |μ - μ₀| / σ. Para diseñar estudio: fijar α, potencia deseada (0.8 o 0.9), estimar σ y tamaño de efecto esperado → calcular n necesario. Trade-off: α vs β, n vs costo.

---

## 45 - Contraste para media (Z/t), proporción, varianza (chi-cuadrado)
*U4*

Media σ conocido: Z = (x̄ - μ₀) / (σ/√n). Media σ desconocido: t = (x̄ - μ₀) / (s/√n) con n-1 gl. Proporción: Z = (p̂ - p₀) / √(p₀q₀/n) (requiere np₀>5, nq₀>5). Varianza: χ² = (n-1)s² / σ₀² con n-1 gl (población Normal). Dos medias independientes: t o Z según σ conocidas. Dos medias pareadas: t sobre diferencias d̄.

---

## 46 - Contraste de dos medias (independientes/pareadas) y dos proporciones
*U4*

Dos medias independientes (σ desconocidas, varianzas iguales): t = (x̄₁ - x̄₂) / sₚ·√(1/n₁+1/n₂) con sₚ² = [(n₁-1)s₁²+(n₂-1)s₂²]/(n₁+n₂-2) y n₁+n₂-2 gl. Varianzas desiguales (Welch): t con gl ajustados. Dos medias pareadas: t = d̄ / (s_d/√n) con n-1 gl. Dos proporciones: Z = (p̂₁ - p̂₂) / √(p̂p̂q̂(1/n₁+1/n₂)) con p̂p̂ = (x₁+x₂)/(n₁+n₂).

---
