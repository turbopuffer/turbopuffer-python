from turbopuffer.backend import make_request

test_data = {
  "ids": [1, 2, 3],
  "vectors": [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
  "attributes": {"key1": ["one", "two", "three"], "key2": ["a", "b", "c"]}
}

def test_list_vectors():
    print()
    response = make_request('vectors', 'hello_world', payload=test_data)
    print('Upsert: ', response)
    response = make_request('vectors', 'hello_world')
    print('List: ', response)
    response = make_request('vectors', 'hello_world', method='DELETE')
    print('Delete: ', response)
