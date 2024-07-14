from qdrant_client import QdrantClient, models
import streamlit as st
import os

qdrant_url = st.secrets.get("QDRANT_URL", os.getenv("QDRANT_URL"))
vector_size = st.secrets.get("VECTOR_SIZE", os.getenv("VECTOR_SIZE"))

client = QdrantClient(location=qdrant_url, timeout=20)


def create_collection(name):
    client.create_collection(
        collection_name=name,
        vectors_config=models.VectorParams(
            size=vector_size, distance=models.Distance.COSINE
        ),
        optimizers_config=models.OptimizersConfigDiff(memmap_threshold=20000),
    )


def delete_collection(name):
    client.delete_collection(name)


def get_collections():
    collections_response = client.get_collections()
    return [collection.name for collection in collections_response.collections]


def get_collection_points(collection_name, point_ids):
    return client.retrieve(collection_name=collection_name, ids=point_ids)


def scroll_collection_points(collection_name, limit=100):
    points = []
    offset = None
    while True:
        response = client.scroll(
            collection_name=collection_name,
            limit=limit,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        points.extend(response[0])
        offset = response[1]
        if offset is None:
            break
    return points


def delete_point(collection_name, point_id):
    client.delete(
        collection_name=collection_name,
        points_selector=models.PointIdsList(points=[point_id]),
    )
