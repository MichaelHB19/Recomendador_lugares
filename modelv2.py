from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, PayloadSchemaType
from sentence_transformers import SentenceTransformer
import pandas as pd
import uuid

# Configuración
QDRANT_URL = "https://864d492f-9299-4b59-97e1-6b560cd4968c.us-east4-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.4yY96naXAXj70PoFhY8h7qrRT5FAXXJ5o6kTkQowfyk"
COLLECTION_NAME = "lugares_con_subtipo"

# Cargar modelo
model = SentenceTransformer('all-MiniLM-L6-v2')

# Conectar a QDrant
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=120)

# Leer dataset
df = pd.read_csv("dataset/FULL_Inventario_MOD.csv", encoding="latin-1", sep=";")
df.columns = df.columns.str.strip().str.lower()
df.rename(columns={'región': 'region'}, inplace=True)
print("Columnas cargadas:", df.columns)

# Crear/Recrear colección
if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(collection_name=COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Crear índice para 'region' como KEYWORD
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="region",
    field_schema=PayloadSchemaType.KEYWORD
)

# Generar puntos y vectorizar
points = []
for _, row in df.iterrows():
    texto = f"{row['region']} - {row['nombre']} - {row['subtipo']} - {row['contenido']}"
    vector = model.encode(texto).tolist()
    points.append(PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload={
            "region": row['region'],
            "nombre": row['nombre'],
            "subtipo": row['subtipo'],
            "contenido": row['contenido']
        }
    ))

BATCH_SIZE = 500
for i in range(0, len(points), BATCH_SIZE):
    batch = points[i:i+BATCH_SIZE]
    client.upsert(collection_name=COLLECTION_NAME, points=batch)
    print(f"subidos puntos {i} a {i + len(batch)}")

print("Datos indexados en:", COLLECTION_NAME)
