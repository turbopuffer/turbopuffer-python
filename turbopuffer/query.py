import sys
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union


class FilterMatch(Enum):
    EQ = "Eq"
    NOT_EQ = "NotEq"
    IN = "In"
    GLOB = "Glob"
    NOT_GLOB = "NotGlob"


FilterTuple = Tuple[FilterMatch, Union[List[str], str, Union[List[int], int]]]


@dataclass
class VectorQuery:
    vector: Optional[List[float]] = None
    distance_metric: Optional[str] = None
    top_k: int = 10
    include_vectors: bool = False
    include_attributes: Optional[Union[List[str], bool]] = None
    filters: Optional[Dict[str, List[FilterTuple]]] = None
    rank_by: Optional[List[Union[str, List[str]]]] = None

    def from_dict(source: dict) -> "VectorQuery":
        return VectorQuery(
            vector=source.get("vector"),
            distance_metric=source.get("distance_metric"),
            top_k=source.get("top_k"),
            include_vectors=source.get("include_vectors"),
            include_attributes=source.get("include_attributes"),
            filters=source.get("filters"),
            rank_by=source.get('rank_by')
        )

    def __post_init__(self):
        if self.vector is not None:
            if "numpy" in sys.modules and isinstance(
                self.vector, sys.modules["numpy"].ndarray
            ):
                if self.vector.ndim != 1:
                    raise ValueError(
                        f"VectorQuery.vector must a 1d-array, got {self.vector.ndim} dimensions"
                    )
            elif not isinstance(self.vector, list):
                raise ValueError(
                    "VectorQuery.vector must be a list, got:", type(self.vector)
                )
        if self.include_attributes is not None:
            if not isinstance(self.include_attributes, list) and not isinstance(
                self.include_attributes, bool
            ):
                raise ValueError(
                    "VectorQuery.include_attributes must be a list or bool, got:",
                    type(self.include_attributes),
                )
        if self.filters is not None:
            if not isinstance(self.filters, dict):
                raise ValueError(
                    "VectorQuery.filters must be a dict, got:", type(self.filters)
                )
            else:
                for name, filter in self.filters.items():
                    if isinstance(filter, list):
                        if len(filter) == 2 and isinstance(filter[0], str):
                            # Support passing a single filter instead of a list
                            self.filters[name] = [filter]
                        elif len(filter) > 0 and not isinstance(filter[0], list):
                            raise ValueError(
                                f"VectorQuery.filters expected a list of filters for key {name}, got list of:",
                                type(filter[0]),
                            )
                    else:
                        raise ValueError(
                            f"VectorQuery.filters expected a list for key {name}, got:",
                            type(filter),
                        )
        if self.rank_by is not None:
            if not isinstance(self.rank_by, list):
                raise ValueError('VectorQuery.rank_by must be a list, got:', type(self.rank_by))
            for item in self.rank_by:
                if not isinstance(item, str) and not isinstance(item, list):
                    raise ValueError('VectorQuery.rank_by elements must be strings or lists, got:', type(item))
