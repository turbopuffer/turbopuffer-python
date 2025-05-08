from dataclasses import dataclass
import sys
from typing import Any, Optional, List, Iterable, Tuple, Union, Dict
from typing_extensions import Literal
from turbopuffer.vectors import VectorRow

# Refer to turbopuffer docs for valid operator names
FilterOperator = str

FilterValue = Union[str, int, List[str], List[int]]
FilterCondition = Tuple[str, FilterOperator, FilterValue]

LegacyFilterCondition = Tuple[FilterOperator, FilterValue]
LegacyFilterDict = Dict[str, List[LegacyFilterCondition]]

Filters = Union[Tuple[str, List["Filters"]], FilterCondition, LegacyFilterDict]

RankInputVector = Tuple[Literal['vector'], Literal['ANN'], List[float]]

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
    RankInputVector,
    RankInputTextQuery,
    RankInputOrderByAttribute,
    List[Union[str, List[str]]],
]

ConsistencyDict = Dict[Literal['level'], Literal['strong', 'eventual']]

@dataclass
class VectorQuery:
    rank_by: RankInput
    distance_metric: Optional[str] = None
    top_k: int = 10
    include_attributes: Optional[Union[List[str], bool]] = None
    filters: Optional[Filters] = None
    consistency: Optional[ConsistencyDict] = None
    vector_encoding: Optional[str] = None

    def from_dict(source: dict) -> 'VectorQuery':
        return VectorQuery(
            distance_metric=source.get('distance_metric'),
            top_k=source.get('top_k'),
            include_attributes=source.get('include_attributes'),
            filters=source.get('filters'),
            rank_by=source.get('rank_by'),
            consistency=source.get('consistency'),
            vector_encoding=source.get('vector_encoding'),
        )

    def __post_init__(self):
        if self.rank_by is None:
            raise ValueError('VectorQuery.rank_by is required')
        if len(self.rank_by) == 3 and self.rank_by[:2] == ['vector', 'ANN']:
            vector = self.rank_by[2]
            if 'numpy' in sys.modules and isinstance(vector, sys.modules['numpy'].ndarray):
                if vector.ndim != 1:
                    raise ValueError(f'VectorQuery.vector must be a 1d array, got {self.vector.ndim} dimensions')
            elif not isinstance(vector, list):
                raise ValueError('VectorQuery.rank_by vector must be a list, got:', type(vector))
        if self.include_attributes is not None:
            if not isinstance(self.include_attributes, list) and not isinstance(self.include_attributes, bool):
                raise ValueError('VectorQuery.include_attributes must be a list or bool, got:', type(self.include_attributes))
        if self.filters is not None:
            if not isinstance(self.filters, dict) and not isinstance(self.filters, list) and not isinstance(self.filters, tuple):
                raise ValueError('VectorQuery.filters must be a dict, tuple, or list, got:', type(self.filters))
        if self.consistency is not None:
            if not isinstance(self.consistency, dict) or 'level' not in self.consistency:
                raise ValueError("VectorQuery.consistency must be a dict with a 'level' key")
            if self.consistency['level'] not in ('strong', 'eventual'):
                raise ValueError("VectorQuery.consistency level must be 'strong' or 'eventual', got:", self.consistency['level'])


@dataclass
class QueryBilling:
    billable_logical_bytes_queried: int
    billable_logical_bytes_returned: int

    def from_dict(source: dict) -> 'QueryBilling':
        return QueryBilling(
            billable_logical_bytes_queried=source['billable_logical_bytes_queried'],
            billable_logical_bytes_returned=source['billable_logical_bytes_returned'],
        )


@dataclass
class QueryResult:
    rows: List[VectorRow]
    performance: Dict[str, Any]
    billing: QueryBilling

    def from_dict(source: dict) -> 'QueryResult':
        return QueryResult(
            rows=[VectorRow.from_dict_v2(row) for row in source['rows']],
            performance=source['performance'],
            billing=QueryBilling.from_dict(source['billing']),
        )
