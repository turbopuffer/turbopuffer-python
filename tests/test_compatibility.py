import turbopuffer as tpuf
import tests

try:
    import numpy as np

    def test_numpy_support():
        ns = tpuf.Namespace(tests.test_prefix + 'numpy')
        data = np.random.uniform(low=-1.5, high=1.5, size=(100, 64))

        # Test column upsert
        ns.write(
            upsert_columns={
                "id": np.arange(0, data.shape[0]),
                "vector": data
            }
        )
        vecs = ns.vectors()
        for i, vec in enumerate(vecs):
            assert vec.id == i
            assert np.allclose(vec.vector, data[i])

        # Test row upsert
        ns.write(
            upsert_rows=[{"id": i, "vector":row} for i, row in enumerate(data)],
        )
        vecs = ns.vectors()
        for i, vec in enumerate(vecs):
            assert vec.id == i
            assert np.allclose(vec.vector, data[i])

        # Test list of numpy data
        ns.write(
            upsert_columns={
                "id": [np.int64(i) for i in range(0, data.shape[0])],
                "vector": [[np.float64(v) for v in row] for row in data]
            }
        )
        vecs = ns.vectors()
        for i, vec in enumerate(vecs):
            assert vec.id == i
            assert np.allclose(vec.vector, data[i])

        # Test query with numpy vector
        result = ns.query(rank_by=["vector", "ANN", data[5]], top_k=1, include_attributes=['vector'])
        assert len(result.rows) == 1
        assert result.rows[0].id == 5
        assert np.allclose(result.rows[0].vector, data[5])

        ns.delete_all()

    print('Loaded numpy tests')
except ImportError:
    print('Skipped numpy tests')

def test_base_url_compatibility():
    assert tpuf.backend.clean_base_url("https://domain/v1/") == "https://domain"
    assert tpuf.backend.clean_base_url("https://domain/v1") == "https://domain"
    assert tpuf.backend.clean_base_url("https://domain/") == "https://domain"
    assert tpuf.backend.clean_base_url("https://domain") == "https://domain"
