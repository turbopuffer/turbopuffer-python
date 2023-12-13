from dataclasses import dataclass
from typing import Optional, Union, List, Iterable, Annotated, Dict
from annotated_types import Ge
from dataclass_wizard import JSONSerializable
from dataclasses import asdict

class Cursor(str):
    pass

@dataclass
class VectorRow(JSONSerializable, str=False): # Prevent JSON pretty printing of data
    id: Annotated[int, Ge(0)]
    vector: Optional[List[float]] = None
    attributes: Optional[Dict[str, str]] = None

    class _(JSONSerializable.Meta):
        skip_defaults = True
        key_transform_with_dump='SNAKE'

    def __init__(self, id: Annotated[int, Ge(0)], vector: Optional[List[float]] = None, attributes: Optional[Dict[str, str]] = None):
        if not isinstance(id, int):
            raise ValueError('Wrong data type passed to VectorRow')
        self.id = id
        self.vector = vector
        self.attributes = attributes

@dataclass
class VectorColumns(JSONSerializable, str=False): # Prevent JSON pretty printing of data
    ids: List[Annotated[int, Ge(0)]]
    vectors: List[List[float]]
    attributes: Dict[str, List[str]]

    class _(JSONSerializable.Meta):
        skip_defaults = True
        key_transform_with_dump='SNAKE'

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
        elif isinstance(row_data, Iterable):
            if not isinstance(row_data, list):
                row_data = list(row_data)
            col_count = len(row_data)
            for i, row in enumerate(row_data):
                if isinstance(row, dict):
                    parsed_row = VectorRow.from_dict(row)
                elif isinstance(row, VectorRow):
                    parsed_row = row
                else:
                    raise NotImplementedError(f'Unsupported row data type: {type(row).name}')

                ids += [parsed_row.id]
                vectors += [parsed_row.vector]
                if parsed_row.attributes:
                    for k, v in parsed_row.attributes.items():
                        attrs = attributes.setdefault(k, [None]*col_count)
                        attrs[i] = v
        else:
            raise NotImplementedError(f'Unsupported row data type: {type(row_data).name}')
        return VectorColumns(ids=ids, vectors=vectors, attributes=attributes)

DATA = Union[Iterable[dict], dict, VectorRow, 'VectorIterator']
SET_DATA = Union[Iterable[VectorRow], VectorColumns]

class VectorIterator:
    namespace: Optional['Namespace'] = None
    data: Optional[SET_DATA] = None
    next_cursor: Optional[Cursor] = None

    def __init__(self, initial_data: Optional[DATA] = None, namespace: Optional['Namespace'] = None, next_cursor: Optional[Cursor] = None):
        self.namespace = namespace
        self.next_cursor = next_cursor

        if initial_data:
            if isinstance(initial_data, list):
                if isinstance(initial_data[0], dict):
                    self.data = [VectorRow.from_dict(row) for row in initial_data]
                elif isinstance(initial_data[0], VectorRow):
                    self.data = initial_data
                else:
                    raise NotImplementedError(f'Unsupported list data type: {type(initial_data[0]).name}')
            elif isinstance(initial_data, dict):
                self.data = VectorColumns.from_dict(initial_data)
            elif isinstance(initial_data, VectorColumns):
                self.data = initial_data
            elif isinstance(initial_data, Iterable):
                raise NotImplementedError(f'VectorIterator from Iterable not yet supported.')
            else:
                raise NotImplementedError(f'Unsupported data type: {type(initial_data).name}')

    def __str__(self) -> str:
        return str({
            'data': self.data,
            'namespace': self.namespace.name,
            'next_cursor': self.next_cursor
        })

    def __iter__(self) -> 'VectorIterator':
        return self

    def __next__(self):
        if self.data is not None:
            it, self.data = self.data, None
            return it
        elif self.next_cursor is None:
            raise StopIteration
        else:
            next_iter = self.namespace.vectors(cursor=self.next_cursor)
            self.next_cursor = next_iter.next_cursor
            return next_iter.data
