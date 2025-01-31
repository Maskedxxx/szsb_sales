import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from core.models.key_selection import KeySelectionParseModel, KeySelectionValidationModel
from utils.logger import logger
from pydantic import ValidationError

@dataclass
class KeySelectionConfig:
    """Configuration for key selection process."""
    model_name: str
    temperature: float = 0
    max_retries: int = 2

@dataclass
class KeySelectionPromptTemplate:
    """Template for LLM prompts."""
    system: str
    user: str

class KeySelectionService:
    """Service for selecting relevant keys using LLM."""
    
    def __init__(
        self,
        client,
        config: KeySelectionConfig,
        prompt_template: KeySelectionPromptTemplate
    ):
        self.client = client
        self.config = config
        self.prompt_template = prompt_template
        
    @staticmethod
    def _format_keys_with_descriptions(
        key_descriptions: Dict[str, str]
    ) -> str:
        """Format keys and descriptions for prompt."""
        return "\n".join(
            f"{key}: {desc}"
            for key, desc in key_descriptions.items()
        )

    def _log_input_keys(self, key_descriptions: Dict[str, str]) -> None:
        """Log input keys with truncated descriptions."""
        key_logs = [
            f"\t{k}: {v[:50] + '...' if len(v) > 50 else v}"
            for k, v in key_descriptions.items()
        ]
        logger.info("Input keys with descriptions:\n" + "\n".join(key_logs))

    def _log_response_obj(self, obj_str: str):
        """Log the fields of the response model object"""
        logger.info(f"KeySelection response: \n {json.dumps(json.loads(obj_str), indent=4, ensure_ascii=False)}")
        

    def _prepare_messages(
        self,
        query: str,
        key_descriptions: Dict[str, str]
    ) -> List[Dict[str, str]]:
        """Prepare messages for LLM prompt."""
        keys_text = self._format_keys_with_descriptions(key_descriptions)
        return [
            {"role": "system", "content": self.prompt_template.system},
            {
                "role": "user",
                "content": self.prompt_template.user.format(
                    query=query,
                    keys=keys_text
                )
            }
        ]

    def _get_model_response(
        self,
        messages: List[Dict[str, str]]
    ) -> Optional[dict]:
        """Get and parse response from LLM."""
        logger.info(
            f"Running key selection model: {self.config.model_name}"
        )
        
        response = self.client.beta.chat.completions.parse(
            temperature=self.config.temperature,
            model=self.config.model_name,
            messages=messages,
            response_format=KeySelectionParseModel,
        )
        
        if response.choices and response.choices[0].message:
            self._log_response_obj(response.choices[0].message.content)

            return response.choices[0].message
        else: 
            return None

    def _process_response(
        self,
        response: Optional[dict],
        allowed_keys: List[str]
    ) -> List[str]:
        """Process and validate model response."""
        if not response:
            return []

        if response.refusal:
            logger.warning(f"Model refused to select: {response.refusal}")
            return []

        try:
            validated = KeySelectionValidationModel.model_validate(
                obj=response.parsed.model_dump(),
                context={"allowed_keys": allowed_keys}
            )
            logger.info(f"Selected keys: {validated.keys}")
            return validated.keys
        except ValidationError as e:
            logger.error(f"Response validation failed: {e}")
            return []
        

    def select_relevant_keys(
        self,
        query: str,
        key_descriptions: Dict[str, str]
    ) -> List[str]:
        """
        Select most relevant keys based on user query using LLM.

        Args:
            query: User query text
            key_descriptions: Dictionary mapping key names to descriptions

        Returns:
            List of selected keys relevant to user query
        """
        self._log_input_keys(key_descriptions)
        
        try:
            messages = self._prepare_messages(query, key_descriptions)
            response = self._get_model_response(messages)
            return self._process_response(response, list(key_descriptions.keys()))
        except Exception as e:
            logger.error(f"Failed to select keys: {e}")
            return []