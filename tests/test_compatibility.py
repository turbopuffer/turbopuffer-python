import turbopuffer as tpuf
import tests

try:
    import numpy as np

    def test_numpy_support():
        ns = tpuf.Namespace('numpy')
        data = np.random.uniform(low=-1.5, high=1.5, size=(100, 64))

        # Test column upsert
        # ns.upsert(
        #     ids=np.arange(0, data.shape[0]),
        #     vectors=data
        # )

        # Test row upsert
        ns.upsert([tpuf.VectorRow(id=i, vector=row) for i, row in enumerate(data)])

        # Test list of numpy data
        ns.upsert(
            ids=[np.int64(i) for i in range(0, data.shape[0])],
            vectors=[[np.float64(v) for v in row] for row in data]
        )

        vecs = ns.vectors()
        for i, vec in enumerate(vecs):
            assert vec.id == i
            assert np.allclose(vec.vector, data[i])

        result = ns.query(vector=data[5].tolist(), distance_metric="cosine_distance", top_k=1, include_vectors=True)
        assert len(result) == 1
        assert result[0].id == 5
        assert np.allclose(result[0].vector, data[5])

        ns.delete_all()

    print('Loaded numpy tests')
except ImportError:
    print('Skipped numpy tests')
