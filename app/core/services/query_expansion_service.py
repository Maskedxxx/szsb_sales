# app/core/services/query_expansion_service.py

"""
Service for expanding user query into a set of similar sub-questions.
"""

from dataclasses import dataclass
import logging
import os
import json
from openai import OpenAI
from typing import Dict, List, Optional
from app.data import PROMPT_QUERY_EXPANSION
from pydantic import BaseModel


@dataclass
class QueryExpansionConfig:
    """Configuration for query expansion service."""
    model_name: str = os.getenv("QUERY_EXPANSION_MODEL")
    temperature=0.2
    max_retries=2
    max_tokens=2048


@dataclass
class QueryExpansionPromptTemplate:
    """Prompt template for LLM."""
    system=PROMPT_QUERY_EXPANSION["system"]
    user=PROMPT_QUERY_EXPANSION["user"]


class QueryExpansionParseModel(BaseModel):
    """Model for parsing LLM response."""
    expanded_queries: List[str]


class QueryExpansionService:
    """
    Service for expanding user query into a set of similar sub-questions,
    preserving the semantics of the original query.
    """
    
    def __init__(
        self,
        client=None,
        config=None,
        prompt_template=None,
        logger=None
    ):
        """
        Initialize query expansion service.
        
        Args:
            client: Client for LLM API
            config: Configuration for model requests
            prompt_template: Prompt template for LLM
        """
        self.client = client or OpenAI(base_url=os.path.join(os.getenv("PROVIDER_BASE_URL"), 'v1'),
            api_key=os.getenv("PROVIDER_API_KEY"),
            timeout=60.0)
        
        self.config = config or QueryExpansionConfig()
        self.prompt_template = prompt_template or QueryExpansionPromptTemplate()
        self.logger = logger or logging.getLogger(__name__)
    
    def _log_response(self, response_content: str) -> None:
        """
        Log model response.
        
        Args:
            response_content: Content of model response
        """
        try:
            parsed_content = json.loads(response_content)
            self.logger.info(f"QueryExpansion response: \n{json.dumps(parsed_content, indent=4, ensure_ascii=False)}")
        except json.JSONDecodeError:
            self.logger.warning(f"Could not parse response as JSON: {response_content}")
    
    def _prepare_messages(self, query: str) -> List[Dict[str, str]]:
        """
        Prepare messages for LLM prompt.
        
        Args:
            query: Original user query
            
        Returns:
            List of messages for LLM request
        """
        return [
            {"role": "system", "content": self.prompt_template.system},
            {"role": "user", "content": self.prompt_template.user.format(query=query)}
        ]
    
    def _get_model_response(self, messages: List[Dict[str, str]]) -> Optional[Dict]:
        """
        Get and parse response from LLM.
        
        Args:
            messages: List of messages for LLM request
            
        Returns:
            Model response or None in case of error
        """
        self.logger.info(f"Running query expansion with model: {self.config.model_name}")
        
        try:
            response = self.client.beta.chat.completions.parse(
                temperature=self.config.temperature,
                model=self.config.model_name,
                messages=messages,
                response_format=QueryExpansionParseModel,
                max_tokens=self.config.max_tokens
            )
            
            if response.choices and response.choices[0].message:
                self._log_response(response.choices[0].message.content)
                return response.choices[0].message
            else:
                self.logger.warning("Empty response from LLM")
                return None
        except Exception as e:
            self.logger.error(f"Error getting model response: {str(e)}")
            return None
    
    def _process_response(self, response: Optional[Dict]) -> List[str]:
        """
        Process model response.
        
        Args:
            response: Model response
            
        Returns:
            List of expanded queries
        """
        if not response:
            self.logger.warning("No response to process")
            return []
        
        if hasattr(response, 'refusal') and response.refusal:
            self.logger.warning(f"Model refused to expand query: {response.refusal}")
            return []
        
        try:
            # Extract and return list of expanded queries
            if hasattr(response, 'parsed') and hasattr(response.parsed, 'expanded_queries'):
                return response.parsed.expanded_queries
            else:
                self.logger.warning("Response format does not contain expanded_queries")
                return []
        except Exception as e:
            self.logger.error(f"Error processing response: {str(e)}")
            return []
    
    def expand_query(self, query: str) -> List[str]:
        """
        Expand user query into a set of similar sub-questions.
        
        Args:
            query: Original user query
            
        Returns:
            List of expanded queries
        """
        try:
            self.logger.info(f"Expanding query: {query}")
            
            messages = self._prepare_messages(query)
            response = self._get_model_response(messages)
            expanded_queries = self._process_response(response)
            
            # If expanded queries could not be obtained, return original query
            if not expanded_queries:
                self.logger.warning("Failed to expand query, returning original query")
                return [query]
            
            # Check that we got exactly 6 sub-questions
            if len(expanded_queries) != 6:
                self.logger.warning(f"Expected 6 expanded queries, got {len(expanded_queries)}")
            
            self.logger.info(f"Query expanded into {len(expanded_queries)} variations")
            return expanded_queries
            
        except Exception as e:
            self.logger.error(f"Error expanding query: {str(e)}")
            return [query]  # Return original query in case of error