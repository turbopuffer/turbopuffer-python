# Code generated by turbopuffer-apigen. DO NOT EDIT.

from typing import Any, Tuple, Union, Literal, Sequence, TypedDict

AggregateBy = Tuple[Literal["Count"], str]
ExprRefNew = TypedDict("ExprRefNew", {"$ref_new": str})
Expr = ExprRefNew
Filter = Union[
    Tuple[str, Literal["Eq"], Any],
    Tuple[str, Literal["NotEq"], Any],
    Tuple[str, Literal["In"], Any],
    Tuple[str, Literal["NotIn"], Any],
    Tuple[str, Literal["Contains"], Any],
    Tuple[str, Literal["NotContains"], Any],
    Tuple[str, Literal["ContainsAny"], Any],
    Tuple[str, Literal["NotContainsAny"], Any],
    Tuple[str, Literal["Lt"], Any],
    Tuple[str, Literal["Lte"], Any],
    Tuple[str, Literal["Gt"], Any],
    Tuple[str, Literal["Gte"], Any],
    Tuple[str, Literal["Glob"], str],
    Tuple[str, Literal["NotGlob"], str],
    Tuple[str, Literal["IGlob"], str],
    Tuple[str, Literal["NotIGlob"], str],
    Tuple[str, Literal["ContainsAllTokens"], str],
    Tuple[str, Literal["ContainsAllTokens"], Sequence[str]],
    Tuple[Literal["Not"], "Filter"],
    Tuple[Literal["And"], Sequence["Filter"]],
    Tuple[Literal["Or"], Sequence["Filter"]],
]
RankByVector = Tuple[str, Literal["ANN"], Sequence[float]]
RankByText = Union[
    Tuple[str, Literal["BM25"], str],
    Tuple[str, Literal["BM25"], Sequence[str]],
    Tuple[Literal["Sum"], Sequence["RankByText"]],
    Tuple[Literal["Max"], Sequence["RankByText"]],
    Tuple[Literal["Product"], Tuple[float, "RankByText"]],
    Tuple[Literal["Product"], Tuple["RankByText", float]],
]
RankByAttributeOrder = Union[Literal["asc"], Literal["desc"]]
RankByAttribute = Tuple[str, RankByAttributeOrder]
RankBy = Union[RankByVector, RankByText, RankByAttribute]
