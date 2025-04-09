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
        return VectorRow(
            id=source.get('id'),
            vector=source.get('vector'),
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


@dataclass
class VectorColumns:
    """
    The VectorColumns type represents a set of vectors stored in a column-oriented layout with their attributes.

    If the VectorColumns is a response from a query, it may also have a set of distance weightings for each vector.
    """

    ids: Union[List[int], List[str]]
    vectors: List[Optional[Union[List[float], str]]]
    attributes: Optional[Dict[str, List[Optional[Union[str, int]]]]] = None

    distances: Optional[List[float]] = None

    def from_dict(source: dict) -> 'VectorColumns':
        return VectorColumns(
            ids=source.get('ids') or [],
            vectors=source.get('vectors') or [],
            attributes=source.get('attributes'),
            distances=source.get('distances'),
        )

    def __post_init__(self):
        if 'numpy' in sys.modules and isinstance(self.ids, sys.modules['numpy'].ndarray):
            if self.ids.ndim != 1:
                raise ValueError(f'VectorColumns.ids must be a 1d array, got {self.ids.ndim} dimensions')
        elif not isinstance(self.ids, list):
            raise ValueError('VectorColumns.ids must be a list, got:', type(self.ids))
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
        row = VectorRow(self.ids[index], self.vectors[index], dist=(self.distances and self.distances[index]))
        if self.attributes:
            row.attributes = dict()
            for key, values in self.attributes.items():
                if values and len(values) > index:
                    if values[index] is not None:
                        row.attributes[key] = values[index]
        return row

    def __iadd__(self, other) -> 'VectorColumns':
        return self.append(other)

    @overload
    def append(self, other: VectorRow) -> 'VectorColumns':
        ...

    @overload
    def append(self, other: List[VectorRow]) -> 'VectorColumns':
        ...

    @overload
    def append(self, other: 'VectorColumns') -> 'VectorColumns':
        ...

    def append(self, other) -> 'VectorColumns':
        old_len = len(self.ids)
        if isinstance(other, VectorRow):
            self.ids.append(other.id)
            self.vectors.append(other.vector)
            if other.dist is not None:
                self.distances.append(other.dist)
            new_len = len(self.ids)
            if other.attributes:
                if not self.attributes:
                    self.attributes = dict()
                for k, v in other.attributes.items():
                    attrs = self.attributes.setdefault(k, [None]*old_len)
                    attrs.append(v)
            if self.attributes:
                for v in self.attributes.values():
                    if len(v) < new_len:
                        v.append(None)
        elif isinstance(other, VectorColumns):
            self.ids.extend(other.ids)
            self.vectors.extend(other.vectors)
            self.distances.extend(other.distances)
            new_len = len(self.ids)
            if other.attributes:
                if not self.attributes:
                    self.attributes = dict()
                for k, v in other.attributes.items():
                    attrs = self.attributes.setdefault(k, [None]*old_len)
                    attrs.extend(v)
            if self.attributes:
                for v in self.attributes.values():
                    if len(v) < new_len:
                        v.extend([None] * (new_len-len(v)))
            return self
        elif isinstance(other, list):
            if len(other) == 0:
                return self
            if isinstance(other[0], VectorRow):
                self.ids.extend(row.id for row in other)
                self.vectors.extend(row.vector for row in other)
                self.distances.extend(row.dist for row in other)
                new_len = len(self.ids)
                if not self.attributes:
                    self.attributes = dict()
                for i, row in enumerate(other):
                    if row.attributes:
                        for k, v in row.attributes.items():
                            attrs = self.attributes.setdefault(k, [None]*new_len)
                            attrs[old_len + i] = v
                for v in self.attributes.values():
                    if len(v) < new_len:
                        v.extend([None] * (new_len-len(v)))
                return self
            else:
                raise ValueError('VectorColumns.append unsupported list type:', type(other[0]))
        else:
            raise ValueError('VectorColumns.append unsupported type:', type(other))

    def from_rows(row_data: Union[List, VectorRow, Iterable[VectorRow]]) -> 'VectorColumns':
        ids = []
        vectors = []
        attributes = {}
        distances = []
        if isinstance(row_data, VectorRow):
            ids = [row_data.id]
            vectors = [row_data.vector]
            distances = [row_data.dist]
            if row_data.attributes:
                for k, v in row_data.attributes.items():
                    attributes[k] = [v]
            return VectorColumns(ids=ids, vectors=vectors, attributes=attributes, distances=distances)
        elif isinstance(row_data, list):
            col_count = len(row_data)
            for i, row in enumerate(row_data):
                if isinstance(row, dict):
                    parsed_row = VectorRow.from_dict(row)
                elif isinstance(row, VectorRow):
                    parsed_row = row
                else:
                    raise ValueError(f'Unsupported row data type: {type(row)}')

                ids += [parsed_row.id]
                vectors += [parsed_row.vector]
                distances += [parsed_row.dist]
                if parsed_row.attributes:
                    for k, v in parsed_row.attributes.items():
                        attrs = attributes.setdefault(k, [None]*col_count)
                        attrs[i] = v
        elif isinstance(row_data, Iterable):
            raise ValueError('VectorColumns from Iterable not yet supported.')
        else:
            raise ValueError(f'Unsupported row data type: {type(row_data)}')
        return VectorColumns(ids=ids, vectors=vectors, attributes=attributes, distances=distances)


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
