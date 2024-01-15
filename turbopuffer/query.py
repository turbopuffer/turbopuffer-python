from dataclasses import dataclass
import sys
from typing import Optional, List, Tuple, Union, Dict
from enum import Enum


class FilterMatch(Enum):
    EQ = 'Eq'
    NOT_EQ = 'NotEq'
    IN = 'In'
    GLOB = 'Glob'
    NOT_GLOB = 'NotGlob'


FilterTuple = Tuple[FilterMatch, Union[List[str], str, Union[List[int], int]]]


@dataclass
class VectorQuery:
    vector: Optional[List[float]] = None
    distance_metric: Optional[str] = None
    top_k: int = 10
    include_vectors: bool = False
    include_attributes: Optional[List[str]] = None
    filters: Optional[Dict[str, List[FilterTuple]]] = None

    def from_dict(source: dict) -> 'VectorQuery':
        return VectorQuery(
            vector=source.get('vector'),
            distance_metric=source.get('distance_metric'),
            top_k=source.get('top_k'),
            include_vectors=source.get('include_vectors'),
            include_attributes=source.get('include_attributes'),
            filters=source.get('filters'),
        )

    def __post_init__(self):
        if self.vector is not None:
            if 'numpy' in sys.modules and isinstance(self.vector, sys.modules['numpy'].ndarray):
                if self.vector.ndim != 1:
                    raise ValueError(f'VectorQuery.vector must a 1d-array, got {self.vector.ndim} dimensions')
            elif not isinstance(self.vector, list):
                raise ValueError('VectorQuery.vector must be a list, got:', type(self.vector))
        if self.include_attributes is not None and not isinstance(self.include_attributes, list):
            raise ValueError('VectorQuery.include_attributes must be a list, got:', type(self.include_attributes))
        if self.filters is not None and not isinstance(self.filters, dict):
            raise ValueError('VectorQuery.filters must be a dict, got:', type(self.filters))
