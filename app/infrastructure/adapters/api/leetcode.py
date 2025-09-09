from typing import Dict, Final, override
from app.domain.ports.api.leetcode import GetProblemDetailsPort
from app.domain.shared.exception.api.api_exception import LeetCodeApiError
from app.domain.shared.leetcode.models import LeetCodeProblem, LeetCodeProblemDetails
import requests
from cattrs import Converter


class GetProblemDetailsAdapter(GetProblemDetailsPort):

    def __init__(self, get_problem_details_endpoint: str):
        self.get_problem_details_endpoint = get_problem_details_endpoint

    @override
    def get_problem_details(self, converter: Converter, payload: Dict[str, str]) -> LeetCodeProblemDetails:
        try:
            request = requests.get(self.get_problem_details_endpoint, params=payload)
            if request.status_code != 200:
                raise LeetCodeApiError()
            return converter.structure(request.json(), LeetCodeProblemDetails)
        except Exception as e:
            raise LeetCodeApiError()