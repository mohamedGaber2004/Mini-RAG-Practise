from qdrant_client import models, QdrantClient
from ..vectorDBInterface import VectorDBInterface
from ..vectorDBEnums import DistanceMethodEnums
from src.models.db_schemas import RetrievedDocument
import logging
from typing_extensions import List

class QdrantDB(VectorDBInterface):
    def __init__(self, db_client: str, default_vector_size: int = 786, distance_method: str = None, index_threshold: int=100):
        self.client = None
        self.db_client = db_client
        self.distance_method = None
        self.default_vector_size = default_vector_size

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger('uvicorn')

    async def connect(self):
        self.client = QdrantClient(path=self.db_client)

    async def disconnect(self):
        self.client = None

    async def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)

    async def list_all_collections(self) -> List:
        return self.client.get_collections()

    async def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name) 

    async def delete_collection(self, collection_name: str):
        if self.is_collection_existed(collection_name=collection_name):
            return self.client.delete_collection(collection_name=collection_name)

    async def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool=False):
        if do_reset:
            _ = self.delete_collection(collection_name=collection_name)

        if not self.is_collection_existed(collection_name=collection_name):
            self.logger.info(f"Creating new Qdrant collection: {collection_name}")
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size, 
                    distance=self.distance_method
                )
            )

            return True
        
        return False

    async def insert_one(self, collection_name: str, texts: str, vectors: list, metadata: list=None, record_ids: str=None):
        if not self.is_collection_existed(collection_name=collection_name):
            self.logger(f"Can't insert new record to non-existed collection : {collection_name} collection.")
            return False
        try:
            _ = self.client.upload_collection(
                collection_name=collection_name,
                ids=[record_ids],
                vectors=[vectors],
                payload=[
                    {
                        "text": texts,
                        "metadata": metadata
                    }
                ]
            )
        except Exception as e :
            self.logger.error(f"Error while inserting batch: {e}")
            return False
        
        return True

    async def insert_many(self, collection_name: str, texts: list, vectors: list, metadata: list=None, record_ids: list=None, batch_size: int=50):
        if not self.is_collection_existed(collection_name=collection_name):
            self.logger(
                f"Can't insert new records to non-existed collection: "
                f"{collection_name} collection."
            )
            return False


        if len(texts) != len(vectors):
            raise ValueError("texts and vectors must have the same length.")

        if metadata is not None and len(metadata) != len(texts):
            raise ValueError("metadata and texts must have the same length.")

        if record_ids is not None and len(record_ids) != len(texts):
            raise ValueError("record_ids and texts must have the same length.")

        if metadata is None:
            metadata = [{} for _ in texts]

        payload = [
            {
                "text": text,
                "metadata": meta
            }
            for text, meta in zip(texts, metadata)
        ]

        try:
            self.client.upload_collection(
                collection_name=collection_name,
                vectors=vectors,
                payload=payload,
                ids=record_ids,
                batch_size=batch_size,
                wait=True
            )
        except Exception as e :
            self.logger.error(f"Error while inserting batch: {e}")
            return False

        return True

    async def search_by_vector(self, collection_name: str, vector: list, limit: int=5):
        results = self.client.query_points(
            collection_name=collection_name,
            limit=limit,
            query=vector
        )

        results_dict = results.model_dump()

        points = results_dict.get("points", [])

        if not points:
            return []

        return [
            RetrievedDocument(
                score=point["score"],
                text=point["payload"]["text"]
            )
            for point in points
        ] 