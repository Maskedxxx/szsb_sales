# tests/test_reranking_service

from dotenv import load_dotenv
load_dotenv('envs/.env.dev.local', override=True)

import pytest
import openai

from app.data.prompts import PROMPT_RERANK_ROU
from app.core.services import RerankingConfig, RerankingPromptTemplate, RerankingService
from app.core.service_models import RouteRerankingParseModel
from app.utils import logger


@pytest.fixture
def reranking_service():
    client = openai.Client(api_key="sk-fake123")

    config = RerankingConfig(
        model_name="MOCKMODEL",
        max_tokens=2048
    )

    prompt_template = RerankingPromptTemplate(
            system=PROMPT_RERANK_ROU["system"],
            user=PROMPT_RERANK_ROU["user"]
    )

    return RerankingService(client=client, config=config, prompt_template=prompt_template, logger=logger)

TEST_CASES_RERANK_ROUTES = [
    pytest.param(
        {
            "cheese_for_meat_products": "some cool description for cheese_for_meat_products",
            "geleon_multifunctional_systems": "some cool description for geleon_multifunctional_systems",
            "marinades": "some cool description for marinades"
        },
        ["geleon_multifunctional_systems"],
        ["geleon_multifunctional_systems"],
        id="one_valid_key_selected"
    ), 
    pytest.param(
        {
            "cheese_for_meat_products": "some cool description for cheese_for_meat_products",
            "geleon_multifunctional_systems": "some cool description for geleon_multifunctional_systems",
            "marinades": "some cool description for marinades"
        },
        ["straciatella"],
        [],
        id="no_valid_keys_selected"
    ),
]


@pytest.mark.parametrize("given_routes, reranked_routes, valid_routes", TEST_CASES_RERANK_ROUTES)
def test_rerank_routes(
    given_routes,
    reranked_routes,
    valid_routes,
    reranking_service: RerankingService ,
    mock_response_factory, monkeypatch):
    
    parsed_model = RouteRerankingParseModel(
        reasoning_step_by_step = ["Some reasoning step.","Another reasoning step.","A third reasoning step"],
        reason="Final reason.",
        reranked_routes=reranked_routes
    )

    mock_parsed_completion = mock_response_factory(
        response_message_content=parsed_model.model_dump_json(),
        model_class=RouteRerankingParseModel,
        model_instance = parsed_model
    )

    def mock_parse(*args, **kwargs):
        return mock_parsed_completion
    
    monkeypatch.setattr(
        "openai.resources.beta.chat.Completions.parse",
        mock_parse
    )

    keys = reranking_service.rerank_routes(
        query='some user query',
        routes=given_routes
    )

    assert sorted(keys)==sorted(valid_routes)