from pathlib import Path
from typing import TypedDict

type CatalogCol = list[str]
type CatalogColName = str


class CatalogInstance(TypedDict):
    name: str
    path: Path
    data: dict[CatalogColName, CatalogCol]
