from typing import Protocol, TypeVar

from app.features.models import Feature, FeatureRequest, FeatureResponse
from app.features.testcase.v1.generator.generator import TestCaseGenerator
from pydantic import BaseModel

Request = TypeVar('Request', bound=FeatureRequest)
Response = TypeVar('Response', bound=FeatureResponse)

class FeatureService(Protocol[Request,Response]):
    async def handleRequest(self, request: Request) -> Response: ...

_service_registry: dict[Feature, FeatureService] = {
    Feature.TEST_CASE_GENERATION: TestCaseGenerator()
}

async def dispatch(feature: Feature, request: FeatureRequest) -> FeatureResponse:
    return await _service_registry[feature].handleRequest(request)