# Recomendador_lugares
# Sistema de Recomendación de Lugares Turísticos

Este proyecto utiliza embeddings semánticos y una base de datos vectorial para recomendar lugares turísticos del Perú a partir de una consulta en lenguaje natural.

## Tecnologías utilizadas

- **Python 3.11+**
- **Qdrant Cloud** (vector database)
- **SentenceTransformers** (`all-MiniLM-L6-v2`)
- **Pandas**
- **PyCharm** (opcional, para desarrollo)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/MichaelHB19/Recomendador_lugares.git
cd proyecto-recomendador

```

### 2. Crear entorno virtual

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```
### 3. Instalar dependencias

Con el entorno activo:

```bash
pip install -r requirements.txt
```
O bien:

```bash
pip install qdrant-client sentence-transformers pandas
```
## Uso del sistema

### 1. Indexar los datos (solo una vez o tras actualizar el CSV)

```bash
python modelv2.py
```
### 2. Ejecutar el buscador

```bash
python busquedav2.py
```
Interactúa desde consola escribiendo:

```bash
LIMA, danzas andinas
```
Si se escribe una palabra en MAYÚSCULAS, el sistema la interpreta como una región y aplica un filtro por esa zona.

El resto del texto se analiza semánticamente para encontrar lugares similares.

