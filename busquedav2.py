from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer

# Configuración
QDRANT_URL = "https://864d492f-9299-4b59-97e1-6b560cd4968c.us-east4-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.4yY96naXAXj70PoFhY8h7qrRT5FAXXJ5o6kTkQowfyk"
COLLECTION_NAME = "lugares_con_subtipo"

# Cargar cliente y modelo
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Escribe tu búsqueda ('salir' para terminar)\n")

while True:
    query = input("Ingrese palabras clave (ej: LIMA, danzas andinas): ").strip()

    if query.lower() in ['salir', 'exit', 'quit']:
        print("Hasta pronto")
        break

    # Detectar región (en mayúsculas) y texto semántico
    words = [w.strip() for w in query.split(",") if w.strip()]
    region = None
    semantic_parts = []
    for w in words:
        if w.isupper():
            region = w.capitalize() #Capitalizar region
        else:
            semantic_parts.append(w)

    query_text = " ".join(semantic_parts)
    query_vector = model.encode(query_text).tolist()

    # Construir filtro solo si hay región
    filtro = Filter(
        must=[FieldCondition(key="region", match=MatchValue(value=region))]
    ) if region else None

    # Usar el argumento correcto: query_vector
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        query_filter=filtro,
        limit=5
    )

    # Mostrar resultados
    if search_result:
        print("\nRecomendaciones encontradas:\n")
        for result in search_result:
            payload = result.payload
            print(f"📍 {payload['nombre']} ({payload['region']} - {payload['subtipo']})")
            print(f"   {payload['contenido']}\n")
    else:
        print("No se encontraron resultados.\n")
