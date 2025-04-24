# tests/test_key_selection_service

import json
from dotenv import load_dotenv
load_dotenv('envs/.env.dev.local', override=True)

import pytest
import openai

from app.data.prompts import PROMPT_SELECT_KEY
from app.core.services import KeySelectionConfig, KeySelectionPromptTemplate, KeySelectionService
from app.core.service_models import KeySelectionParseModel
from app.utils import logger


@pytest.fixture
def key_selection_service():
    client = openai.Client(api_key="sk-fake123")

    config = KeySelectionConfig(
        model_name="MOCKMODEL",
        max_tokens=2048
    )

    prompt_template = KeySelectionPromptTemplate(
            system=PROMPT_SELECT_KEY["system"],
            user=PROMPT_SELECT_KEY["user"]
    )

    return KeySelectionService(client=client, config=config, prompt_template=prompt_template, logger=logger)

TEST_CASES_SELECT_RELEVANT_KEYS = [
    pytest.param(
        {
            "lakomka_ice_cream": "some cool description for lakomka",
            "plombir_ice_cream": "some cool description for plombir",
            "creme_brulee": "some cool description for creme-brulee"
        },
        ["creme_brulee"],
        ["creme_brulee"],
        id="one_valid_key_selected"
    ),
    pytest.param(
        {
            "lakomka_ice_cream": "some cool description for lakomka",
            "plombir_ice_cream": "some cool description for plombir",
            "creme_brulee": "some cool description for creme-brulee"
        },
        ["straciatella"],
        [],
        id="no_valid_keys_selected"
    ),
]


@pytest.mark.parametrize("given_keys, selected_keys, valid_keys", TEST_CASES_SELECT_RELEVANT_KEYS)
def test_select_relevant_keys(
    given_keys,
    selected_keys,
    valid_keys,
    key_selection_service: KeySelectionService ,
    mock_response_factory, monkeypatch):
    
    parsed_model = KeySelectionParseModel(
        reasoning_step_by_step = ["Some reasoning step.","Another reasoning step.","A third reasoning step"],
        reason="Final reason.",
        selected_keys=selected_keys
    )

    mock_parsed_completion = mock_response_factory(
        response_message_content=parsed_model.model_dump_json(),
        model_class=KeySelectionParseModel,
        model_instance = parsed_model
    )

    def mock_parse(*args, **kwargs):
        return mock_parsed_completion
    
    monkeypatch.setattr(
        "openai.resources.beta.chat.Completions.parse",
        mock_parse
    )

    keys = key_selection_service.select_relevant_keys(
        query='some user query',
        key_descriptions=given_keys
    )

    assert sorted(keys)==sorted(valid_keys)