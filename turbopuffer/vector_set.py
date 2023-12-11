from turbopuffer.vector_space import VectorSpace

class VectorObject(object):
    def __init__(self):
        pass

class VectorSet(list[VectorObject]):
    def __init__(self, vector_space: VectorSpace):
        self.vector_space = vector_space