# Modelos supervisados
>***Recordemos:***   
En los modelos de aprendizaje supervisado se le otorgan respuestas correctas e incorrectas para aprender y descubrir las conexiones entre los elementos.
## 🗂️ Regresion lineal
La regresión lineal es una técnica estadística que se usa para encontrar la relación entre las variables. Encuentran la relación entre las variables y las etiquetas.   
![no-supervisado](../../images/regresion-lineal.png)

## 🗂️ Regresion lineal: Pérdida
La perdida es una métrica que mide la distancia que hay entre las predicciones del modelo y la respuestas certeras.   
Para aprender, al modelo no le importa que la pérdida sea negativa o positiva(dirección), le importa el valor.   

Entre los principales tipos de pérdida tenemos:

-**Pérdida de L1:** Es la suma de los valores absolutos de la diferencia de la predicción y el valor real.   

-**Error absoluto medio(MAE):** Es la media de las pérdidas de L1.

-**Pérdida de L2:** Es la suma de de la diferencia al cuadrado entre los valores predichos y los reales.

-**Error cuadrático medio(ECM):** Es la media de la pérdida de L2.

-**Raiz cuadrada del error cuadrático medio:** Es la raiz cuadrada del error cuadrático medio.

## 🗂️ ¿Cómo elegimos correctamente una función de pérdida?

>MAE    
Si quieremos penalizar menos los errores. Está más lejos de los valores atípicos pero más cerca de la mayoría de otros puntos de datos.   
![no-supervisado](../../images/regresion-lineal-a.png)   

---   

>ECM    
Si queremos pnalizar más los errores. El modelo está más cerca de los valores atípicos pero más lejos de los otros puntos de datos.
![no-supervisado](../../images/regresion-lineal-b.png)  


## 🗂️ ¿Cómo elegimos correctamente una función de pérdida?