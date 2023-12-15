from dataclasses import dataclass
from typing import Optional, List, Tuple, Union, Dict
from dataclass_wizard import JSONSerializable
from enum import Enum

class FilterMatch(Enum):
    EQ = 'Eq'
    NOT_EQ = 'NotEq'
    IN = 'In'
    GLOB = 'Glob'
    NOT_GLOB = 'NotGlob'

@dataclass
class IdFilter(Tuple[FilterMatch, Union[List[int], int]]):
    pass

@dataclass
class AttributeFilter(Tuple[FilterMatch, Union[List[str], str]]):
    pass

@dataclass
class AttributeFilters(JSONSerializable):
    id: Optional[List[IdFilter]]
    attributes: Optional[Dict[str, List[AttributeFilter]]]

    class _(JSONSerializable.Meta):
        skip_defaults = True
        key_transform_with_dump='SNAKE'

@dataclass
class VectorQuery(JSONSerializable):
    vector: Optional[List[float]] = None
    distance_metric: Optional[str] = None
    top_k: int = 10
    include_vectors: bool = False
    include_attributes: Optional[List[str]] = None
    filters: Optional[AttributeFilter] = None

    class _(JSONSerializable.Meta):
        skip_defaults = True
        key_transform_with_dump='SNAKE'
