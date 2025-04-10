from dataclasses import dataclass
from functools import lru_cache
import struct
import sys
import turbopuffer as tpuf
from typing import Optional, Union, List, Iterable, Dict, overload
from itertools import islice


def batch_iter(iterable, n):
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


class Cursor(str):
    pass


@lru_cache(maxsize=64)
def _get_struct(vector_length: int) -> struct.Struct:
    return struct.Struct(f'<{vector_length}f')


def b64encode_vector(vector: List[float]) -> str:
    """
    Encodes a list of floats into a base64 string representation of the float
    array in a little-endian binary format.

    Args:
        vector (List[float]): The list of floats to encode.

    Returns:
        str: The base64 encoded string representation of the vector.
    """
    packed = _get_struct(len(vector)).pack(*vector)
    return tpuf.b64encode_as_string(packed)


def b64decode_vector(encoded: str) -> List[float]:
    """
    Decodes a base64 string representation of a float array in a little-endian
    binary format into a list of floats.

    Args:
        encoded (str): The base64 encoded string representation of the vector.

    Returns:
        List[float]: The decoded list of floats.
    """
    packed = tpuf.b64decode(encoded)
    return list(_get_struct(len(packed)//4).unpack(packed))


@dataclass
class VectorRow:
    """
    The VectorRow type represents a single vector ID, along with its vector values and attributes.

    If the VectorRow is a response from a query, it may also have a distance weighting.
    """

    id: Union[int, str]
    vector: Optional[List[float]] = None
    attributes: Optional[Dict[str, Optional[Union[str, int]]]] = None
    dist: Optional[float] = None

    def from_dict(source: dict) -> 'VectorRow':
        vector = source.get('vector')
        vector_encoding_format = source.get('vector_encoding_format')
        if vector_encoding_format is None or vector_encoding_format == 'float':
            pass # already in float format
        elif vector_encoding_format == 'base64':
            vector = b64decode_vector(vector)
        else:
            raise ValueError(f'Unsupported vector encoding format: {vector_encoding_format}')
        return VectorRow(
            id=source.get('id'),
            vector=vector,
            attributes=source.get('attributes'),
            dist=source.get('dist'),
        )

    def __post_init__(self):
        if not isinstance(self.id, int) and not isinstance(self.id, str):
            raise ValueError('VectorRow.id must be an int or str, got:', type(self.id))
        if self.vector is not None:
            if 'numpy' in sys.modules and isinstance(self.vector, sys.modules['numpy'].ndarray):
                if self.vector.ndim != 1:
                    raise ValueError(f'VectorRow.vector must be a 1d array, got {self.vector.ndim} dimensions')
            elif not isinstance(self.vector, list) and not isinstance(self.vector, str):
                raise ValueError('VectorRow.vector must be a list or string, got:', type(self.vector))
        if self.attributes is not None and not isinstance(self.attributes, dict):
            raise ValueError('VectorRow.attributes must be a dict, got:', type(self.attributes))

    def __str__(self) -> str:
        fields = []
        if isinstance(self.id, int):
            fields.append(f'id={self.id}')
        else:
            fields.append(f"id='{self.id}'")
        fields.append(f'vector={self.vector}')
        if self.attributes:
            fields.append(f'attributes={self.attributes}')
        if self.dist is not None:
            fields.append(f'dist={self.dist}')
        return f"VectorRow({', '.join(fields)})"

    def to_dict_for_write(self) -> dict:
        o = { 'id': self.id }

        if self.vector is not None:
            if tpuf.encode_vectors_as_base64 and isinstance(self.vector, list):
                o['vector'] = b64encode_vector(self.vector)
            else:
                o['vector'] = self.vector

        if self.attributes is not None:
            o.update(self.attributes)

        return o


@dataclass
class VectorColumns:
    """
    The VectorColumns type represents a set of vectors stored in a column-oriented layout with their attributes.

    If the VectorColumns is a response from a query, it may also have a set of distance weightings for each vector.
    """

    ids: Union[List[int], List[str]]
    vectors: Optional[List[Optional[Union[List[float], str]]]] = None
    attributes: Optional[Dict[str, List[Optional[Union[str, int]]]]] = None

    distances: Optional[List[float]] = None

    def from_dict(source: dict) -> 'VectorColumns':
        return VectorColumns(
            ids=source.get('ids') or [],
            vectors=source.get('vectors') or None,
            attributes=source.get('attributes'),
            distances=source.get('distances'),
        )

    def __post_init__(self):
        if 'numpy' in sys.modules and isinstance(self.ids, sys.modules['numpy'].ndarray):
            if self.ids.ndim != 1:
                raise ValueError(f'VectorColumns.ids must be a 1d array, got {self.ids.ndim} dimensions')
        elif not isinstance(self.ids, list):
            raise ValueError('VectorColumns.ids must be a list, got:', type(self.ids))

        if self.vectors is not None:
            if 'numpy' in sys.modules and isinstance(self.vectors, sys.modules['numpy'].ndarray):
                if self.vectors.ndim != 2:
                    raise ValueError(f'VectorColumns.ids must be a 2d array, got {self.vectors.ndim} dimensions')
            elif not isinstance(self.vectors, list):
                raise ValueError('VectorColumns.vectors must be a list, got:', type(self.vectors))
            if len(self.ids) != len(self.vectors):
                raise ValueError('VectorColumns.ids and VectorColumns.vectors must be the same length')

        if self.attributes is not None:
            if not isinstance(self.attributes, dict):
                raise ValueError('VectorColumns.attributes must be a dict, got:', type(self.attributes))
            for key, values in self.attributes.items():
                if not isinstance(values, list):
                    raise ValueError(f'VectorColumns.attributes[{key}] must be a list, got:', type(values))
                if len(values) != len(self.ids):
                    raise ValueError(f'VectorColumns.attributes[{key}] must be the same length as VectorColumns.ids')
        if self.distances is not None and len(self.distances) != len(self.ids):
            raise ValueError('VectorColumns.distances must be the same length as VectorColumns.ids')

    def __str__(self) -> str:
        fields = [
            f'ids={self.ids}',
            f'vectors={self.vectors}',
        ]
        if self.attributes:
            fields.append(f'attributes={self.attributes}')
        if self.distances:
            fields.append(f'distances={self.distances}')
        return f"VectorColumns({', '.join(fields)})"

    def __len__(self) -> int:
        return len(self.ids)

    def __getitem__(self, index) -> VectorRow:
        # This functions as the main mechanism for converting Columns to Rows
        vector = self.vectors[index] if self.vectors is not None else None
        row = VectorRow(self.ids[index], vector, dist=(self.distances and self.distances[index]))
        if self.attributes:
            row.attributes = dict()
            for key, values in self.attributes.items():
                if values and len(values) > index:
                    if values[index] is not None:
                        row.attributes[key] = values[index]
        return row

    def to_dict_for_write(self) -> dict:
        o = { 'id': self.ids }

        if self.vectors is not None:
            if tpuf.encode_vectors_as_base64:
                o['vector'] = [
                    b64encode_vector(vector) if isinstance(vector, list) else vector
                    for vector in self.vectors
                ]
            else:
                o['vector'] = self.vectors

        if self.attributes is not None:
            o.update(self.attributes)

        return o


SET_DATA = Union[Iterable[VectorRow], VectorColumns]
DATA = Union[Iterable[dict], dict, VectorRow, SET_DATA]


class VectorResult:
    """
    The VectorResult type represents a set of vectors that are the result of a query.

    A VectorResult can be treated as either a lazy iterator or a list by the user.
    Reading the length of the result will internally buffer the full result.
    """

    namespace: Optional['Namespace'] = None
    data: Optional[SET_DATA] = None
    index: int = -1
    offset: int = 0
    next_cursor: Optional[Cursor] = None

    performance: Optional[dict] = None

    def __init__(self, initial_data: Optional[DATA] = None, namespace: Optional['Namespace'] = None, next_cursor: Optional[Cursor] = None):
        self.namespace = namespace
        self.index = -1
        self.offset = 0
        self.next_cursor = next_cursor

        self.data = VectorResult.load_data(initial_data)

    def load_data(initial_data: DATA) -> SET_DATA:
        if initial_data:
            if isinstance(initial_data, list):
                if isinstance(initial_data[0], dict):
                    return [VectorRow.from_dict(row) for row in initial_data]
                elif isinstance(initial_data[0], VectorRow):
                    return initial_data
                else:
                    raise ValueError(f'Unsupported list data type: {type(initial_data[0])}')
            elif isinstance(initial_data, dict):
                return VectorColumns.from_dict(initial_data)
            elif isinstance(initial_data, VectorColumns):
                return initial_data
            elif isinstance(initial_data, Iterable):
                raise ValueError('VectorResult from Iterable not yet supported.')
            else:
                raise ValueError(f'Unsupported data type: {type(initial_data)}')

    def __str__(self) -> str:
        if not self.next_cursor and self.offset == 0:
            return str(self.data)
        else:
            return ("VectorResult("
                    f"namespace='{self.namespace.name}', "
                    f"offset={self.offset}, "
                    f"next_cursor='{self.next_cursor}', "
                    f"data={self.data})")

    def __len__(self) -> int:
        assert self.offset == 0, "Can't call len(VectorResult) after iterating"
        assert self.index == -1, "Can't call len(VectorResult) after iterating"
        if not self.next_cursor:
            if self.data is not None:
                return len(self.data)
            return 0
        else:
            it = iter(self)
            self.data = [next for next in it]
            self.offset = 0
            self.index = -1
            self.next_cursor = None
            return len(self.data)

    def __getitem__(self, index) -> VectorRow:
        if index >= len(self.data) and self.next_cursor:
            it = iter(self)
            self.data = [next for next in it]
            self.offset = 0
            self.index = -1
            self.next_cursor = None
        return self.data[index]

    def __iter__(self) -> 'VectorResult':
        assert self.offset == 0, "Can't iterate over VectorResult multiple times"
        return VectorResult(self.data, self.namespace, self.next_cursor)

    def __next__(self):
        if self.data is not None and self.index + 1 < len(self.data):
            self.index += 1
            return self.data[self.index]
        elif self.next_cursor is None:
            raise StopIteration
        else:
            response = self.namespace.backend.make_api_request(
                '/v1/namespaces',
                self.namespace.name,
                query={'cursor': self.next_cursor}
            )
            content = response.get('content', dict())
            self.offset += len(self.data)
            self.index = -1
            self.next_cursor = content.pop('next_cursor', None)
            self.data = VectorResult.load_data(content)
            return self.__next__()
