from dataclasses import dataclass
from typing import Optional, Union, List, Iterable, Dict
from dataclass_wizard import JSONSerializable
from itertools import islice

ITERATOR_BATCH_SIZE = 5_000

def batch_iter(iterable, n):
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch: return
        yield batch

class Cursor(str):
    pass

@dataclass
class VectorRow(JSONSerializable, str=False): # Prevent JSON pretty printing of data
    """
    The VectorRow type represents a single vector ID, along with its vector values and attributes.
    """

    id: int
    vector: Optional[List[float]] = None
    attributes: Optional[Dict[str, str]] = None

    class _(JSONSerializable.Meta):
        skip_defaults = True
        key_transform_with_dump='SNAKE'

    def __post_init__(self):
        if not isinstance(self.id, int):
            raise ValueError('VectorRow.id must be an int, got:', type(self.vector))
        if self.vector is None:
            raise ValueError('VectorRow.vector cannot be None, use Namespace.delete([ids...]) instead.')
        if not isinstance(self.vector, list):
            raise ValueError('VectorRow.vector must be a list, got:', type(self.vector))
        if self.attributes is not None and not isinstance(self.attributes, dict):
            raise ValueError('VectorRow.attributes must be a dict, got:', type(self.attributes))

@dataclass
class VectorColumns(JSONSerializable, str=False): # Prevent JSON pretty printing of data
    """
    The VectorColumns type represents a set of vectors stored in a column-oriented layout.
    """

    ids: List[int]
    vectors: List[Optional[List[float]]]
    attributes: Optional[Dict[str, List[str]]] = None

    class _(JSONSerializable.Meta):
        skip_defaults = True
        key_transform_with_dump='SNAKE'

    def __post_init__(self):
        if not isinstance(self.ids, list):
            raise ValueError('VectorColumns.ids must be a list, got:', type(self.ids))
        if not isinstance(self.vectors, list):
            raise ValueError('VectorColumns.vectors must be a list, got:', type(self.vectors))
        if len(self.ids) != len(self.vectors):
            raise ValueError('VectorColumns.ids and VectorColumns.vectors must be the same length')
        if self.attributes is not None:
            if not isinstance(self.attributes, dict):
                raise ValueError('VectorColumns.attributes must be a dict, got:', type(self.attributes))
            for key, values in self.attributes.items():
                if not isinstance(values, list):
                    raise ValueError(f'VectorColumns.attributes[{key}] must be a list, got:', type(values))

    def __len__(self) -> int:
        return len(self.ids)

    def __getitem__(self, index) -> VectorRow:
        row = VectorRow(self.ids[index], self.vectors[index])
        if self.attributes:
            row.attributes = dict()
            for key, values in self.attributes.items():
                if values and len(values) > index:
                    row.attributes[key] = values[index]
        return row

    def __iadd__(self, other) -> 'VectorColumns':
        return self.append(other)

    def append(self, other) -> 'VectorColumns':
        old_len = len(self.ids)
        if isinstance(other, VectorRow):
            self.ids.append(other.id)
            self.vectors.append(other.vector)
            new_len = len(self.ids)
            if other.attributes:
                if not self.attributes: self.attributes = dict()
                for k, v in other.attributes.items():
                    attrs = self.attributes.setdefault(k, [None]*old_len)
                    attrs.extend(v)
            if self.attributes:
                for v in self.attributes.values():
                    if len(v) < new_len: v.append(None)
        elif isinstance(other, VectorColumns):
            self.ids.extend(other.ids)
            self.vectors.extend(other.vectors)
            new_len = len(self.ids)
            if other.attributes:
                if not self.attributes: self.attributes = dict()
                for k, v in other.attributes.items():
                    attrs = self.attributes.setdefault(k, [None]*old_len)
                    attrs.extend(v)
            if self.attributes:
                for v in self.attributes.values():
                    if len(v) < new_len:
                        v.extend([None] * (new_len-len(v)))
            return self
        elif isinstance(other, list):
            if len(other) == 0: return self
            if isinstance(other[0], VectorRow):
                self.ids.extend(row.id for row in other)
                self.vectors.extend(row.vector for row in other)
                new_len = len(self.ids)
                if not self.attributes: self.attributes = dict()
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
                raise NotImplementedError('VectorColumns.append unsupported list type:', type(other[0]))
        else:
            raise NotImplementedError('VectorColumns.append unsupported type:', type(other))

    def from_rows(row_data: Union[VectorRow, Iterable[VectorRow]]) -> 'VectorColumns':
        ids = []
        vectors = []
        attributes = {}
        if isinstance(row_data, VectorRow):
            ids = [row_data.id]
            vectors = [row_data.vector]
            if row_data.attributes:
                for k, v in row_data.attributes.items():
                    attributes[k] = [v]
            return VectorColumns(ids=ids, vectors=vectors, attributes=attributes)
        elif isinstance(row_data, list):
            col_count = len(row_data)
            for i, row in enumerate(row_data):
                if isinstance(row, dict):
                    parsed_row = VectorRow.from_dict(row)
                elif isinstance(row, VectorRow):
                    parsed_row = row
                else:
                    raise NotImplementedError(f'Unsupported row data type: {type(row)}')

                ids += [parsed_row.id]
                vectors += [parsed_row.vector]
                if parsed_row.attributes:
                    for k, v in parsed_row.attributes.items():
                        attrs = attributes.setdefault(k, [None]*col_count)
                        attrs[i] = v
        elif isinstance(row_data, Iterable):
            raise NotImplementedError(f'VectorColumns from Iterable not yet supported.')
        else:
            raise NotImplementedError(f'Unsupported row data type: {type(row_data)}')
        return VectorColumns(ids=ids, vectors=vectors, attributes=attributes)

DATA = Union[Iterable[dict], dict, VectorRow, 'VectorResult']
SET_DATA = Union[Iterable[VectorRow], VectorColumns]

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
                    raise NotImplementedError(f'Unsupported list data type: {type(initial_data[0])}')
            elif isinstance(initial_data, dict):
                return VectorColumns.from_dict(initial_data)
            elif isinstance(initial_data, VectorColumns):
                return initial_data
            elif isinstance(initial_data, Iterable):
                raise NotImplementedError(f'VectorResult from Iterable not yet supported.')
            else:
                raise NotImplementedError(f'Unsupported data type: {type(initial_data)}')

    def __str__(self) -> str:
        if not self.next_cursor and self.offset == 0:
            return str(self.data)
        else:
            return f"VectorResult(namespace='{self.namespace.name}', offset={self.offset} next_cursor='{self.next_cursor}', data={self.data})"

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
            response = self.namespace.backend.make_api_request('vectors', self.namespace.name, query={'cursor': self.next_cursor})
            self.offset += len(self.data)
            self.next_cursor = response.pop('next_cursor', None)
            self.data = VectorResult.load_data(response)
            return self.__next__()
