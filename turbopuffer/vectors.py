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
            raise ValueError('Wrong data type passed for VectorRow.id')
        if self.vector is not None and not isinstance(self.vector, list):
            raise ValueError('Wrong data type passed for VectorRow.vector')
        if self.attributes is not None and not isinstance(self.attributes, dict):
            raise ValueError('Wrong data type passed for VectorRow.attributes')

@dataclass
class VectorColumns(JSONSerializable, str=False): # Prevent JSON pretty printing of data
    """
    The VectorColumns type represents a set of vectors stored in a column-oriented layout.
    """

    ids: List[int]
    vectors: List[List[float]]
    attributes: Optional[Dict[str, List[str]]] = None

    class _(JSONSerializable.Meta):
        skip_defaults = True
        key_transform_with_dump='SNAKE'

    def __post_init__(self):
        if not isinstance(self.ids, list):
            raise ValueError('Wrong data type passed for VectorColumns.ids')
        if not isinstance(self.vectors, list):
            raise ValueError('Wrong data type passed for VectorColumns.vectors')
        if self.attributes is not None and not isinstance(self.attributes, dict):
            raise ValueError('Wrong data type passed for VectorColumns.attributes')

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

DATA = Union[Iterable[dict], dict, VectorRow, 'VectorIterator']
SET_DATA = Union[Iterable[VectorRow], VectorColumns]

class VectorIterator:
    """
    The VectorIterator type represents a set of vectors that may or may not be lazily loaded in batches from an external source.
    """

    namespace: Optional['Namespace'] = None
    data: Optional[SET_DATA] = None
    index: int = -1
    next_cursor: Optional[Cursor] = None

    def __init__(self, initial_data: Optional[DATA] = None, namespace: Optional['Namespace'] = None, next_cursor: Optional[Cursor] = None):
        self.namespace = namespace
        self.index = -1
        self.next_cursor = next_cursor

        self.data = VectorIterator.load_data(initial_data)

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
                raise NotImplementedError(f'VectorIterator from Iterable not yet supported.')
            else:
                raise NotImplementedError(f'Unsupported data type: {type(initial_data)}')

    def __str__(self) -> str:
        return str({
            'data': 'redacted',#self.data,
            'namespace': self.namespace.name,
            'next_cursor': self.next_cursor
        })

    def __iter__(self) -> 'VectorIterator':
        return self

    def __next__(self):
        if self.data is not None and self.index + 1 < len(self.data):
            self.index += 1
            return self.data[self.index]
        else:
            self.data = None
            self.index = -1
            if self.next_cursor is None:
                raise StopIteration
            else:
                response = self.namespace.backend.make_api_request('vectors', self.namespace.name, query={'cursor': self.next_cursor})
                self.next_cursor = response.pop('next_cursor', None)
                self.data = VectorIterator.load_data(response)
                return self.__next__()
