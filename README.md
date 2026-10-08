# 📚 Data Engineer Bible

Repositorio personal de apuntes, chuletas (*cheatsheets*) y ejercicios para consolidar conocimientos como Data Engineer, con foco en **Python, SQL, AWS y Databricks/GenAI**.

> 🎯 Objetivo: tener un único lugar de referencia rápida para consultar sintaxis, patrones y buenas prácticas antes/durante el día a día profesional.

![Estado](https://img.shields.io/badge/estado-en%20construcción-orange)
![Idioma](https://img.shields.io/badge/idioma-español-blue)
![Foco](https://img.shields.io/badge/foco-SQL%20%C2%B7%20Python%20%C2%B7%20AWS%20%C2%B7%20IA-green)

## 🗂️ Estructura del repositorio

```text
data-engineer-bible/
├── 00-almacenamiento/      # Data Lake, Lakehouse, formatos, Bronze/Silver/Gold
├── 01-sql/                 # De SELECT a subconsultas y CTEs
├── 02-python/              # Fundamentos, ficheros, librerías de datos
├── 03-06/                  # (reservado para futuras secciones)
└── 07-ia/                  # IA y Machine Learning
    ├── 01-fundamentos/
    ├── 02-datos/
    ├── 03-deep-learning/
    └── 04-ml-clasico/
```



---

## 🧰 Stack cubierto

| Categoría | Herramientas |
| --- | --- |
| **Lenguajes** | SQL, Python |
| **Librerías de datos / ML** | NumPy, pandas, scikit-learn, matplotlib, TensorFlow |
| **Cloud** | AWS (Cloud Practitioner como base), Amazon SageMaker |
| **Plataforma de datos** | Databricks, Delta Lake |
| **Arquitectura** | Data Lake, Lakehouse, ETL/ELT, Bronze/Silver/Gold |
| **Transformación y orquestación** | dbt, orquestadores |
| **IA aplicada** | Redes neuronales, embeddings, introducción a LLMs |

---

## 🧪 Ejecutar los notebooks

```bash
# Python 3.12 recomendado (TensorFlow aún no soporta versiones más recientes)
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install numpy pandas scikit-learn matplotlib tensorflow ipykernel
```

Después abre los `.ipynb` con **VS Code** o **Jupyter**.

---

## 📌 Notas

Este repositorio es un documento **vivo**: se actualiza continuamente a medida que avanzo en el aprendizaje y encuentro nuevos casos prácticos en el día a día profesional.   
Para este curso se han seguido bastantes pautas el temario de:   
***https://developers.google.com/machine-learning?hl=es-419***

