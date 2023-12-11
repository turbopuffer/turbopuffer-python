from turbopuffer.vector_set import VectorSet
from typing import Optional

class Cursor(str):
    pass

class VectorSpace:
    def __init__(self, namespace: str, api_key: Optional[str] = None):
        self.namespace = namespace

    def list_vectors(cursor: Optional[Cursor] = None) -> (VectorSet, Optional[Cursor]):
        pass