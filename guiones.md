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
