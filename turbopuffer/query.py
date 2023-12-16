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

FilterTuple = Tuple[FilterMatch, Union[List[str], str, Union[List[int], int]]]

@dataclass
class VectorQuery(JSONSerializable):
    vector: Optional[List[float]] = None
    distance_metric: Optional[str] = None
    top_k: int = 10
    include_vectors: bool = False
    include_attributes: Optional[List[str]] = None
    filters: Optional[Dict[str, List[FilterTuple]]] = None

    class _(JSONSerializable.Meta):
        skip_defaults = True
        key_transform_with_dump='SNAKE'
