# tests/conftest.py

import time
import pytest
from typing import Any, Dict, Type, TypeVar
from openai.types.chat import (
    ParsedChoice,
    ParsedChatCompletion,
    ParsedChatCompletionMessage
)

T = TypeVar("T")

@pytest.fixture
def mock_response_factory():
    """
    Returns a factory function that can build a
    ParsedChatCompletion[ModelType], given:
      - response_message_content (str)
      - model_class (Type[T])
    """
    def _factory(response_message_content: str, model_class: Type[T], model_instance: T) -> ParsedChatCompletion[T]:
        """
        Build a mock ParsedChatCompletion[model_class].
        """
        return ParsedChatCompletion[model_class](
            id='mockchatcmpl-042',
            created=int(time.time()),
            model='MOCKMODEL',
            choices=[
                ParsedChoice[model_class](
                    index=0,
                    message=ParsedChatCompletionMessage[model_class](
                        parsed=model_instance,
                        content=response_message_content,
                        role='assistant'
                    ),
                    finish_reason='stop'
                )
            ],
            object='chat.completion'
        )

    return _factory

