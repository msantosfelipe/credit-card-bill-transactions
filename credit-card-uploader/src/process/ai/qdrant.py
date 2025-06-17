import uuid, os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance


CATEGORIES_COLLECTION = "categories"


def update_qdrant_collection(categories_dict):
    collections = client.get_collections().collections
    names = [c.name for c in collections]
    exists = CATEGORIES_COLLECTION in names
    outdated = True

    if exists:
        info = client.get_collection(CATEGORIES_COLLECTION)
        print(info)
        print("Total de categorias:", len(categories_dict))
        print("Total de vetores:", info.points_count)
        
        if info.points_count == 0 or info.points_count == len(categories_dict):
            outdated = False

    if outdated:
        print("[INFO] Qdrant - refreshing collection")
        client.recreate_collection(
            collection_name=CATEGORIES_COLLECTION,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

        points = []
        for description, category in categories_dict.items():
            vector = embedder.encode(description).tolist()

            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "description": description,
                    "category": category
                }
            ))
        else:
            print("[INFO] Qdrant - collection up to date")

        print(len(points))
        client.upsert(collection_name=CATEGORIES_COLLECTION, points=points)


def _init_qdrant_client():
    print("[INFO] Initializing Qdrant client")
    return QdrantClient(host=os.environ.get("QDRANT_HOST"), port=os.environ.get("QDRANT_PORT"))


def _init_qdrant_model():
    print("[INFO] Initializing Qdrant model")
    return SentenceTransformer(os.environ.get("QDRANT_MODEL"))


client = _init_qdrant_client()
embedder = _init_qdrant_model()
