from dataclasses import dataclass
import sys
from typing import Optional, List, Tuple, Union, Dict
from typing import Iterable
from typing_extensions import Literal

# Refer to turbopuffer docs for valid operator names
FilterOperator = str

FilterValue = Union[str, int, List[str], List[int]]
FilterCondition = Tuple[str, FilterOperator, FilterValue]

LegacyFilterCondition = Tuple[FilterOperator, FilterValue]
LegacyFilterDict = Dict[str, List[LegacyFilterCondition]]

Filters = Union[Tuple[str, List["Filters"]], FilterCondition, LegacyFilterDict]

RankInputTextQuery = Union[
    Tuple[str, Literal['BM25'], str],
    Tuple[Literal['Sum'], Iterable['RankInputTextQuery']],
    Tuple[Literal['Product'], Tuple[float, Iterable['RankInputTextQuery']]],
    Tuple[Literal['Product'], Tuple[Iterable['RankInputTextQuery'], float]],
]

AttributeOrdering = Union[Literal['asc'], Literal['desc']]

RankInputOrderByAttribute = Tuple[str, AttributeOrdering]

# Uses tuples for nice typing, but also allows arrays for backwards compatibility
RankInput = Union[
    RankInputTextQuery,
    RankInputOrderByAttribute,
    List[Union[str, List[str]]],
]

ConsistencyDict = Dict[Literal['level'], Literal['strong', 'eventual']]

@dataclass
class VectorQuery:
    vector: Optional[List[float]] = None
    distance_metric: Optional[str] = None
    top_k: int = 10
    include_vectors: bool = False
    include_attributes: Optional[Union[List[str], bool]] = None
    filters: Optional[Filters] = None
    rank_by: Optional[RankInput] = None
    consistency: Optional[ConsistencyDict] = None

    def from_dict(source: dict) -> 'VectorQuery':
        return VectorQuery(
            vector=source.get('vector'),
            distance_metric=source.get('distance_metric'),
            top_k=source.get('top_k'),
            include_vectors=source.get('include_vectors'),
            include_attributes=source.get('include_attributes'),
            filters=source.get('filters'),
            rank_by=source.get('rank_by'),
            consistency=source.get('consistency'),
        )

    def __post_init__(self):
        if self.vector is not None:
            if 'numpy' in sys.modules and isinstance(self.vector, sys.modules['numpy'].ndarray):
                if self.vector.ndim != 1:
                    raise ValueError(f'VectorQuery.vector must be a 1d array, got {self.vector.ndim} dimensions')
            elif not isinstance(self.vector, list):
                raise ValueError('VectorQuery.vector must be a list, got:', type(self.vector))
        if self.include_attributes is not None:
            if not isinstance(self.include_attributes, list) and not isinstance(self.include_attributes, bool):
                raise ValueError('VectorQuery.include_attributes must be a list or bool, got:', type(self.include_attributes))
        if self.filters is not None:
            if not isinstance(self.filters, dict) and not isinstance(self.filters, list) and not isinstance(self.filters, tuple):
                raise ValueError('VectorQuery.filters must be a dict, tuple, or list, got:', type(self.filters))
        if self.rank_by is not None:
            if not isinstance(self.rank_by, list) and not isinstance(self.rank_by, tuple):
                raise ValueError('VectorQuery.rank_by must be a list or tuple, got:', type(self.rank_by))
            for item in self.rank_by:
                if not isinstance(item, str) and not isinstance(item, list) and not isinstance(item, tuple):
                    raise ValueError('VectorQuery.rank_by elements must be strings, tuples or lists, got:', type(item))
        if self.consistency is not None:
            if not isinstance(self.consistency, dict) or 'level' not in self.consistency:
                raise ValueError("VectorQuery.consistency must be a dict with a 'level' key")
            if self.consistency['level'] not in ('strong', 'eventual'):
                raise ValueError("VectorQuery.consistency level must be 'strong' or 'eventual', got:", self.consistency['level'])
