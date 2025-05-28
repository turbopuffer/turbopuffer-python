import struct
from typing import List

import pybase64

from turbopuffer._utils._utils import lru_cache


@lru_cache(maxsize=64)
def _get_struct(vector_length: int) -> struct.Struct:
    return struct.Struct(f"<{vector_length}f")


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
    return pybase64.b64encode_as_string(packed)


def b64decode_vector(encoded: str) -> List[float]:
    """
    Decodes a base64 string representation of a float array in a little-endian
    binary format into a list of floats.

    Args:
        encoded (str): The base64 encoded string representation of the vector.

    Returns:
        List[float]: The decoded list of floats.
    """
    packed = pybase64.b64decode(encoded, validate=True)
    return list(_get_struct(len(packed) // 4).unpack(packed))
