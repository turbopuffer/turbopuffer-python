from turbopuffer.vectors import Cursor, VectorIterator, VectorColumns, VectorRow, DATA
from turbopuffer.backend import make_api_request
from turbopuffer.query import VectorQuery
from typing import Optional, Iterable, Union

class Namespace:
    name: str
    api_key: Optional[str]

    def __init__(self, name: str, api_key: Optional[str] = None):
        self.name = name
        self.api_key = api_key

    def __str__(self) -> str:
        return f'tpuf-namespace:{self.name}'

    def upsert(self, data: DATA) -> None:
        # print(f'Upsert data ({type(data)}):', data)
        if data is None:
            raise ValueError('upsert input data cannot be None')
        elif isinstance(data, list):
            return self.upsert(VectorColumns.from_rows(data))
        elif isinstance(data, dict):
            if 'id' in data:
                response = make_api_request('vectors', self.name, api_key=self.api_key, payload=VectorColumns.from_rows(VectorRow.from_dict(data)))
            elif 'ids' in data:
                response = make_api_request('vectors', self.name, api_key=self.api_key, payload=VectorColumns.from_dict(data))
            else:
                raise ValueError('Provided dict is missing ids.')
        elif isinstance(data, VectorColumns):
            response = make_api_request('vectors', self.name, api_key=self.api_key, payload=data)
        elif isinstance(data, VectorRow):
            response = make_api_request('vectors', self.name, api_key=self.api_key, payload=VectorColumns.from_rows(data))
        elif isinstance(data, Iterable):
            raise NotImplementedError('Upsert with Iterable not yet supported.')
        else:
            raise NotImplementedError(f'Unsupported data type: {type(data).name}')

        if (response.get('status', '') != 'OK'): print('Upsert response:', response)
        assert response.get('status', '') == 'OK'

    def query(self, query_data: Union[dict, VectorQuery]):
        if not isinstance(query_data, VectorQuery):
            if isinstance(query_data, dict):
                query_data = VectorQuery.from_dict(query_data)
            else:
                raise ValueError(f'query input type must be compatible with turbopuffer.VectorQuery: {type(query_data).name}')

        response = make_api_request('vectors', self.name, 'query', payload=query_data)
        return VectorIterator(response, namespace=self)

    def vectors(self, cursor: Optional[Cursor] = None) -> VectorIterator:
        response = make_api_request('vectors', self.name, cursor=cursor)
        next_cursor = response.pop('next_cursor', None)
        return VectorIterator(response, namespace=self, next_cursor=next_cursor)

    def delete_all(self) -> None:
        response = make_api_request('vectors', self.name, api_key=self.api_key, method='DELETE')
        if (response.get('status', '') != 'ok'): print('Delete all response:', response)
        assert response.get('status', '') == 'ok'