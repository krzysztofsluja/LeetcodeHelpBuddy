from enum import Enum, auto
from typing import Any, ClassVar
from pydantic import BaseModel

class Feature(Enum):
    TEST_CASE_GENERATION = auto()

class FeatureRequest(BaseModel):
    feature: Feature
    __dataclass_fields__: ClassVar[dict[str, Any]]

class FeatureResponse(BaseModel):
    feature: Feature
    __dataclass_fields__: ClassVar[dict[str, Any]]


