from typing import (
    IO,
    Any,
    AsyncIterable,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Pattern,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import httpx2

URL = Tuple[
    bytes,  # scheme
    bytes,  # host
    Optional[int],  # port
    bytes,  # path
]
Headers = List[Tuple[bytes, bytes]]
Content = Union[str, bytes, Iterable[bytes], AsyncIterable[bytes]]

HeaderTypes = Union[
    httpx2.Headers,
    Dict[str, str],
    Dict[bytes, bytes],
    Sequence[Tuple[str, str]],
    Sequence[Tuple[bytes, bytes]],
]
CookieTypes = Union[Dict[str, str], Sequence[Tuple[str, str]]]

DefaultType = TypeVar("DefaultType", bound=Any)

URLPatternTypes = Union[str, Pattern[str], URL, httpx2.URL]
QueryParamTypes = Union[
    bytes, str, List[Tuple[str, Any]], Dict[str, Any], Tuple[Tuple[str, Any], ...]
]

ResolvedResponseTypes = Optional[Union[httpx2.Request, httpx2.Response]]
RouteResultTypes = Union[ResolvedResponseTypes, Awaitable[ResolvedResponseTypes]]
CallableSideEffect = Callable[..., RouteResultTypes]
SideEffectListTypes = Union[httpx2.Response, Exception, Type[Exception]]
SideEffectTypes = Union[
    CallableSideEffect,
    Exception,
    Type[Exception],
    Iterator[SideEffectListTypes],
]

# Borrowed from HTTPX2's "private" types.
FileContent = Union[IO[bytes], bytes, str]
FileTypes = Union[
    # file (or bytes)
    FileContent,
    # (filename, file (or bytes))
    Tuple[Optional[str], FileContent],
    # (filename, file (or bytes), content_type)
    Tuple[Optional[str], FileContent, Optional[str]],
    # (filename, file (or bytes), content_type, headers)
    Tuple[Optional[str], FileContent, Optional[str], Mapping[str, str]],
]
RequestFiles = Union[Mapping[str, FileTypes], Sequence[Tuple[str, FileTypes]]]
