from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Property:
    name: str
    type: str
    nullable: bool = True
    collection: bool = False
    reference: Optional[str] = None


@dataclass
class Entity:
    name: str
    namespace: str
    kind: str
    properties: List[Property] = field(default_factory=list)
    description: str = ""


@dataclass
class Metadata:
    entities: Dict[str, Entity] = field(default_factory=dict)
