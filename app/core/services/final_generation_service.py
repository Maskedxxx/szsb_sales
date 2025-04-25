# app/core/services/final_generation_service.py

from dataclasses import dataclass
import logging
from typing import Dict, List, Optional

@dataclass
class FinalGenerationConfig:
    """Configuration for OpenAI API calls."""
    model_name: str
    temperature: float = 0.1
    top_p: float = 0.95,
    max_retries: int = 2,
    max_tokens: int = 4096

@dataclass
class FinalGenerationPromptTemplate:
    """Template for LLM prompts."""
    system: str
    user: str

class FinalGenerationService:
    """Service for final response generation using LLM."""
    
    def __init__(
        self,
        client,
        config: FinalGenerationConfig,
        prompt_template: FinalGenerationPromptTemplate,
        logger
    ):
        self.client = client
        self.config = config
        self.prompt_template = prompt_template
        self.logger = logger or logging.getLogger(__name__)

    def _prepare_messages(
        self,
        question: str,
        context:str 
    ) -> List[Dict[str, str]]:
        """Prepare messages for LLM prompt."""
        return [
            {"role": "system", "content": self.prompt_template.system},
            {
                "role": "user",
                "content": self.prompt_template.user.format(
                    question=question,
                    content=context
                )
            }
        ]
    
    def _get_model_response(
            self,
            messages: List[Dict[str, str]]
            ) -> Optional[dict]:
        self.logger.info(
            f"Running final answer generation model: {self.config.model_name}"
        )
        response = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )

        return response
    
    def _process_response(
        self,
        response: Optional[dict]
    ) -> List[str]:
        """Process and validate model response."""
        if not response:
            return None

        if response.refusal:
            self.logger.warning(f"Model refused to select: {response.refusal}")
            return None
        

    def generate_final_answer(
        self,
        question: str,
        context: str
        ):
        messages = self._prepare_messages(question, context)
        response = self._get_model_response(messages=messages)

        if response.choices and response.choices[0].message:
            self.logger.info(f"----- Final answer -----\n{response.choices[0].message.content}")

            return response.choices[0].message
        else: 
            return None
