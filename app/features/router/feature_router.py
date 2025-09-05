from typing import Protocol, TypeVar

from app.features.models import Feature, FeatureRequest, FeatureResponse
from app.features.testcase.v1.service.testcase_service import TestCaseGenerationService

Request = TypeVar('Request', bound=FeatureRequest)
Response = TypeVar('Response', bound=FeatureResponse)

class FeatureService(Protocol[Request,Response]):
    async def handleRequest(self, request: Request) -> Response: ...

_service_registry: dict[Feature, FeatureService] = {
    Feature.TEST_CASE_GENERATION: TestCaseGenerationService()
}

async def dispatch(feature: Feature, request: FeatureRequest) -> FeatureResponse:
    print(f"Dispatching request to feature: {feature}")
    return await _service_registry[feature].handleRequest(request)