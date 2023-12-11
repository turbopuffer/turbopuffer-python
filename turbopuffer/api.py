from turbopuffer.error import AuthenticationError
from typing import Optional

def read_api_key(api_key: Optional[str] = None) -> str:
    import turbopuffer
    if api_key is not None:
        return api_key
    elif turbopuffer.api_key is not None:
        return turbopuffer.api_key
    else:
        raise AuthenticationError("No turbopuffer API key was provided.\n"
            "Set the TURBOPUFFER_API_KEY environment variable, "
            "or pass `api_key=` when creating a VectorSpace.")
