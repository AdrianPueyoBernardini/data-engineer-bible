# 🚀 Roadmap Personal: De Trainee a AI Engineer & AI Architect

Este repositorio contiene la hoja de ruta de aprendizaje para hacer la transición desde **Computer Vision / ML Tradicional** hacia **IA Generativa (RAG, Agentes)**, sentando las bases para convertirme en **AI Architect**.

---

## 📌 Fase 0: Git & Entornos de Desarrollo (Común)
- [ ] **Git & GitHub/GitLab:** `git clone`, `branch`, `checkout`, `commit`, `push`, `pull`, `merge` y resolución de conflictos por terminal.
- [ ] **Gestión de Entornos en Python:** Creación y gestión de entornos virtuales con `venv` o `conda`.
- [ ] **Manejo de dependencias:** Uso de `requirements.txt` y `pip install`.
- [ ] **Jupyter Notebooks / VS Code:** Configuración y ejecución de notebooks locales para prototipar.

---

## 📌 Fase 1: Python para Data Science & ML (Común)

### Python Base Intermedio
- [ ] **Estructuras de datos:** Manejo avanzado de diccionarios, listas, sets y tuplas.
- [ ] **Comprensión:** List/Dictionary comprehensions.
- [ ] **Funciones & POO:** Funciones `*args`, `**kwargs`, lambdas y creación de clases básicas (`class`, `__init__`).
- [ ] **Manejo de archivos:** Lectura y escritura de `JSON`, `CSV`, `YAML` y `TXT`.
- [ ] **Programación Asíncrona:** Conceptos básicos de `async` / `await` (esencial para llamadas a APIs de IA).

### Librerías de Datos y Computación
- [ ] **NumPy:**
  - [ ] Creación y manipulación de Arrays (1D, 2D, nD).
  - [ ] Operaciones de álgebra lineal básicas: Producto escalar (*dot product*) y norma de un vector.
  - [ ] Indexación y slicing (*broadcasting*).
- [ ] **Pandas:**
  - [ ] Carga de datasets (`read_csv`, `read_json`, `read_excel`).
  - [ ] Limpieza de datos: Manejo de nulos (`fillna`, `dropna`), duplicados y tipos de datos.
  - [ ] Filtrado, selección y transformaciones de columnas.
  - [ ] Agrupaciones y agregaciones con `.groupby()`.
  - [ ] Exportación de datasets estructurados.
- [ ] **Visualización de Datos:**
  - [ ] **Matplotlib:** Creación de gráficos básicos (líneas, barras, dispersión) y visualización de imágenes/bounding boxes con `imshow()`.
  - [ ] *(Opcional)* **Seaborn:** Gráficos estadísticos rápidos (matriz de correlación, distribuciones). *(No prioritario, con Matplotlib basta).*

---

## 📌 Fase 2: Deep Learning & Computer Vision (Común)

### PyTorch Core
- [ ] **Tensores:** Diferencia entre arrays de NumPy y `torch.Tensor`, conversión entre ellos.
- [ ] **Gestión de Hardware:** Envío de tensores y modelos a GPU/CPU (`.to('cuda')`, `.to('cpu')`).
- [ ] **Datasets y DataLoaders:** Creación de pipelines de carga de datos con `Dataset` y `DataLoader`.
- [ ] **Transformaciones:** Manipulación de imágenes con `torchvision.transforms` (resize, normalize, tensor representation).

### Fundamentos de Visión por Computador & Embeddings
- [ ] **Conceptos de CV:** Bounding boxes, formatos de anotación (COCO, Pascal VOC, YOLO format).
- [ ] **Métricas de Evaluación:** Precision, Recall, F1-Score, IoU (Intersection over Union).
- [ ] **Modelos Preentrenados:** Extracción de características (*feature extraction*) usando redes preentrenadas (ResNet, EfficientNet).
- [ ] **Concepto de Embedding:** Entender cómo una imagen o texto se traduce a un vector numérico.
- [ ] **Similitud Vectorial:** Cálculo manual de Similitud del Coseno (*Cosine Similarity*) entre dos vectores.

---

## 📌 Fase 3: IA Generativa & Arquitectura RAG (Común)

### Ecosistema de LLMs
- [ ] **Consumo de APIs de LLMs:** Conexión con SDKs oficiales (`openai`, `anthropic`, o modelos locales vía `ollama`).
- [ ] **Prompt Engineering:** Prompts del sistema, *few-shot prompting*, estructuración de respuestas en JSON.
- [ ] **Text Embeddings:** Generación de embeddings de texto con modelos de HuggingFace (`sentence-transformers`) o OpenAI.

### Bases de Datos Vectoriales & RAG
- [ ] **Vector Databases (Local):** Instalación y uso básico de **ChromaDB** o **FAISS**.
- [ ] **Chunking Strategies:** División de documentos grandes usando *RecursiveCharacterTextSplitter*.
- [ ] **Retrieval-Augmented Generation (RAG) Básico:**
  - [ ] Cargar un documento (PDF/TXT).
  - [ ] Dividir en trozos (*chunks*).
  - [ ] Vectorizar y guardar en DB Vectorial.
  - [ ] Buscar chunks similares a una pregunta.
  - [ ] Enviar prompt al LLM con el contexto recuperado.

### Orquestación de IA
- [ ] **LangChain / LlamaIndex:**
  - [ ] `PromptTemplate` y `ChatPromptTemplate`.
  - [ ] Cadenas con LCEL (LangChain Expression Language: `prompt | llm | output_parser`).
  - [ ] Implementación de un flujo RAG completo con LangChain.
  - [ ] **Memoria:** Gestión del historial de conversación (`ChatMessageHistory`).
  - [ ] **Agentes & Tools:** Crear un agente sencillo que use *Function Calling* o herramientas externas (ej. buscar en Google/calculadora).

### Despliegue de Demostración
- [ ] **Creación de UI Sencilla:** Construir una interfaz rápida con **Streamlit** o **Gradio** para enseñar el proyecto RAG.

---

## 🛠️ OPCIÓN A: PATH AWS (Especialización Cloud & MLOps)

> Elegir este path si el departamento trabaja principalmente sobre AWS o buscas una base sólida de infraestructura dura y MLOps.

### Módulo AWS 1: Infraestructura & Gestión del Dato
- [ ] **AWS IAM:** Configuración de usuarios, roles, políticas de acceso (*Policies*) y claves de API.
- [ ] **AWS S3:** Creación de buckets, subida/descarga de objetos, organización de datasets de imágenes y textos.
- [ ] **AWS Lambda & API Gateway:** Creación de funciones *serverless* sencillas para activar eventos.

### Módulo AWS 2: Machine Learning & Visión (Proyecto Actual)
- [ ] **Amazon SageMaker Ground Truth:** Creación de trabajos de etiquetado y exportación del manifest de datos.
- [ ] **SageMaker Training Jobs:** Entrenamiento de modelos usando contenedores propios o preconfigurados.
- [ ] **SageMaker Endpoints:** Despliegue de modelos entrenados para inferencia en tiempo real y *Serverless Endpoints*.
- [ ] **SageMaker Pipelines:** Automatización del flujo de preparación de datos, entrenamiento y evaluación.

### Módulo AWS 3: IA Generativa en AWS
- [ ] **Amazon Bedrock:** Consumo de modelos generativos (Claude, Llama, Titan) mediante API sin gestionar infraestructura.
- [ ] **Bedrock Knowledge Bases:** Implementación de RAG gestionado directamente dentro del ecosistema de AWS.
- [ ] **Amazon OpenSearch Serverless:** Configuración como base de datos vectorial en AWS.

### 📜 Certificaciones AWS Objetivo
- [ ] **AWS Certified AI Practitioner** *(Iniciación / Teórico)*
- [ ] **AWS Certified Machine Learning - Specialty** o **AWS Certified Data Engineer - Associate** *(Avanzado)*

---

## 🛠️ OPCIÓN B: PATH AZURE (Especialización Cloud & GenAI Enterprise)

> Elegir este path si el departamento está enfocado en soluciones corporativas con Microsoft, OpenAI y rápida integración de negocio.

### Módulo Azure 1: Infraestructura & Gestión del Dato
- [ ] **Azure Portal & CLI:** Estructura de Suscripciones, Grupos de Recursos (*Resource Groups*) y Roles IAM (RBAC).
- [ ] **Azure Blob Storage:** Almacenamiento de contenedores, blobs y gestión de claves de acceso/SAS tokens.
- [ ] **Azure Functions:** Creación de código *serverless* para eventos y webhooks.

### Módulo Azure 2: Machine Learning tradicional
- [ ] **Azure Machine Learning Workspace:** Configuración de entornos de trabajo y cómputos (*Compute Instances/Clusters*).
- [ ] **Azure ML Datasets & Assets:** Registro de conjuntos de datos y control de versiones.
- [ ] **Azure Computer Vision / Custom Vision:** Servicios cognitivos para detección de objetos y clasificación visual.
- [ ] **Azure ML Pipelines:** Definición y ejecución de flujos de trabajo de entrenamiento y despliegue.

### Módulo Azure 3: IA Generativa en Azure
- [ ] **Azure OpenAI Service:** Despliegue y configuración de modelos (GPT-4o, embeddings) en entorno privado empresarial.
- [ ] **Azure AI Search:** Configuración de índices de búsqueda vectorial y búsqueda híbrida (*Vector + Keyword + Semantic Ranker*).
- [ ] **Azure AI Studio:** Creación de flujos RAG, evaluación de modelos y orquestación con Prompt Flow.

### 📜 Certificaciones Azure Objetivo
- [ ] **Microsoft Certified: Azure AI Fundamentals (AI-900)** *(Iniciación / Teórico)*
- [ ] **Microsoft Certified: Azure AI Engineer Associate (AI-102)** *(Avanzado)*