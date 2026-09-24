## 🗂️ Normalización de datos numéricos
Normalizar es extremandamente importante, ayuda a que los modelos de AA converjan más rápido, den mejores predicciones y a evitar la trampa del NaN. Esto se da cuando los valores son tan altos que se abrevia y pierde el valor.   

Podemos encontrar 3 tipos de normalización más populares:
1. Escalamiento lineal
2. Ajuste de la puntuación Z
3. Escalamiento logarítmico   
---

**1. Escalamiento lineal:** Convierte los valores a un rango estandar, generalmente de 0 a 1 o de -1 a 1.   
- Es buena idea el escalamiento lineal. cuando los límites superiores o inferiores no cambian demasiado con el tiempo.
- Cuando contiene pocos valores atípicos
- La función se distribuye de forma uniforme en su rango.   

**2. Ajuste de la puntuación Z:** Una puntuación Z es la cantidad de desviaciones que tiene un valor a partir de la media.   
- Es buena idea cuandio los datos siguen una distribución normal o similar   

**3. Escalamiento logarítmico:** El ajuste de escala logarítmica es útil cuando los datos se ajustan a una distribución de ley de potencias.

**Extra. Recorte:** Con la técnica del recorte delimitamos un valor máximo para limitar los valores extremadamente altos.