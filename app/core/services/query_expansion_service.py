# app/core/services/query_expansion_service.py

"""
Сервис для расширения запроса пользователя в набор похожих подвопросов.
"""

from dataclasses import dataclass
import os
import json
from openai import OpenAI
from typing import Dict, List, Optional
from core.prompts import PROMPT_QUERY_EXPANSION
from pydantic import BaseModel
from utils.logger import logger


@dataclass
class QueryExpansionConfig:
    """Конфигурация для сервиса расширения запросов."""
    model_name: str = os.getenv("QUERY_EXPANSION_MODEL")
    temperature=0.2
    max_retries=2
    max_tokens=2048


@dataclass
class QueryExpansionPromptTemplate:
    """Шаблон промпта для LLM."""
    system=PROMPT_QUERY_EXPANSION["system"]
    user=PROMPT_QUERY_EXPANSION["user"]


class QueryExpansionParseModel(BaseModel):
    """Модель для парсинга ответа от LLM."""
    expanded_queries: List[str]


class QueryExpansionService:
    """
    Сервис для расширения пользовательского запроса в набор похожих подвопросов,
    сохраняющих семантику исходного запроса.
    """
    
    def __init__(
        self,
        client=None,
        config=None,
        prompt_template=None
    ):
        """
        Инициализация сервиса расширения запросов.
        
        Args:
            client: Клиент для работы с LLM API
            config: Конфигурация для запросов к модели
            prompt_template: Шаблон промпта для LLM
        """
        self.client = client or OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        self.config = config or QueryExpansionConfig()
        self.prompt_template = prompt_template or QueryExpansionPromptTemplate()
    
    def _log_response(self, response_content: str) -> None:
        """
        Логирует ответ модели.
        
        Args:
            response_content: Содержимое ответа от модели
        """
        try:
            parsed_content = json.loads(response_content)
            logger.info(f"QueryExpansion response: \n{json.dumps(parsed_content, indent=4, ensure_ascii=False)}")
        except json.JSONDecodeError:
            logger.warning(f"Could not parse response as JSON: {response_content}")
    
    def _prepare_messages(self, query: str) -> List[Dict[str, str]]:
        """
        Подготавливает сообщения для LLM промпта.
        
        Args:
            query: Исходный запрос пользователя
            
        Returns:
            Список сообщений для запроса к LLM
        """
        return [
            {"role": "system", "content": self.prompt_template.system},
            {"role": "user", "content": self.prompt_template.user.format(query=query)}
        ]
    
    def _get_model_response(self, messages: List[Dict[str, str]]) -> Optional[Dict]:
        """
        Получает и парсит ответ от LLM.
        
        Args:
            messages: Список сообщений для запроса к LLM
            
        Returns:
            Ответ от модели или None в случае ошибки
        """
        logger.info(f"Running query expansion with model: {self.config.model_name}")
        
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
                logger.warning("Empty response from LLM")
                return None
        except Exception as e:
            logger.error(f"Error getting model response: {str(e)}")
            return None
    
    def _process_response(self, response: Optional[Dict]) -> List[str]:
        """
        Обрабатывает ответ от модели.
        
        Args:
            response: Ответ от модели
            
        Returns:
            Список расширенных запросов
        """
        if not response:
            logger.warning("No response to process")
            return []
        
        if hasattr(response, 'refusal') and response.refusal:
            logger.warning(f"Model refused to expand query: {response.refusal}")
            return []
        
        try:
            # Извлекаем и возвращаем список расширенных запросов
            if hasattr(response, 'parsed') and hasattr(response.parsed, 'expanded_queries'):
                return response.parsed.expanded_queries
            else:
                logger.warning("Response format does not contain expanded_queries")
                return []
        except Exception as e:
            logger.error(f"Error processing response: {str(e)}")
            return []
    
    def expand_query(self, query: str) -> List[str]:
        """
        Расширяет пользовательский запрос в набор похожих подвопросов.
        
        Args:
            query: Исходный запрос пользователя
            
        Returns:
            Список расширенных запросов
        """
        try:
            logger.info(f"Expanding query: {query}")
            
            messages = self._prepare_messages(query)
            response = self._get_model_response(messages)
            expanded_queries = self._process_response(response)
            
            # Если не удалось получить расширенные запросы, вернем исходный запрос
            if not expanded_queries:
                logger.warning("Failed to expand query, returning original query")
                return [query]
            
            # Проверяем, что получили ровно 6 подвопросов
            if len(expanded_queries) != 6:
                logger.warning(f"Expected 6 expanded queries, got {len(expanded_queries)}")
            
            logger.info(f"Query expanded into {len(expanded_queries)} variations")
            return expanded_queries
            
        except Exception as e:
            logger.error(f"Error expanding query: {str(e)}")
            return [query]  # В случае ошибки возвращаем исходный запрос