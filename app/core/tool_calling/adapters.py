"""
Адаптеры для интеграции с различными LLM сервисами.

Содержит адаптеры для подключения Tool Calling к различным LLM провайдерам.
"""

import json
import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class LLMAdapter(ABC):
    """
    Абстрактный базовый класс для адаптеров LLM.
    
    Позволяет подключать различные LLM провайдеры к системе Tool Calling.
    """
    
    @abstractmethod
    def call_with_tools(self, system_prompt: str, user_query: str, tools: list) -> Optional[Dict[str, Any]]:
        """
        Вызывает LLM с tool calling.
        
        Args:
            system_prompt: Системный промпт для LLM
            user_query: Запрос пользователя
            tools: Список доступных инструментов
            
        Returns:
            Словарь с tool_calls или None если инструменты не выбраны
        """
        pass


class OpenAIAdapter(LLMAdapter):
    """
    Адаптер для работы с OpenAI-совместимыми API.
    
    Поддерживает tool calling через OpenAI API или совместимые сервисы.
    """
    
    def __init__(self, client, model_name: str):
        """
        Инициализация адаптера.
        
        Args:
            client: OpenAI client или совместимый
            model_name: Название модели для использования
        """
        self.client = client
        self.model_name = model_name
        logger.info(f"Инициализирован OpenAI адаптер с моделью: {model_name}")
    
    def call_with_tools(self, system_prompt: str, user_query: str, tools: list) -> Optional[Dict[str, Any]]:
        """
        Вызывает OpenAI API с tool calling.
        
        Args:
            system_prompt: Системный промпт
            user_query: Запрос пользователя
            tools: Список инструментов в формате OpenAI
            
        Returns:
            Словарь с tool_calls или None
        """
        try:
            logger.info(f"Вызов {self.model_name} с tool calling для запроса: {user_query[:100]}...")
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                tools=tools,
                tool_choice="auto",
                max_tokens=1000,
                temperature=0.1
            )
            
            # Проверяем, есть ли tool calls в ответе
            if response.choices[0].message.tool_calls:
                tool_calls = response.choices[0].message.tool_calls
                logger.info(f"LLM вернул {len(tool_calls)} tool calls")
                
                return {
                    "tool_calls": [{
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in tool_calls]
                }
            else:
                logger.info("LLM не вернул tool calls")
                return None
                
        except Exception as e:
            logger.error(f"Ошибка при вызове LLM с tools: {str(e)}")
            return None


class MockAdapter(LLMAdapter):
    """
    Мок-адаптер для тестирования.
    
    Имитирует работу реального LLM для тестирования функциональности.
    """
    
    def __init__(self, responses: Optional[Dict[str, Dict]] = None):
        """
        Инициализация мок-адаптера.
        
        Args:
            responses: Словарь предопределенных ответов {запрос: tool_call}
        """
        self.responses = responses or self._default_responses()
        logger.info("Инициализирован Mock адаптер для тестирования")
    
    def _default_responses(self) -> Dict[str, Dict]:
        """Возвращает предопределенные ответы для тестирования."""
        return {
            "барбекю": {"name": "барбекю"},
            "горчичный": {"name": "горчичный"},
            "бутылка": {"packaging": "бутылка_пластиковая"},
            "калори": {"kbgu": "низкие_до_150"},
            "жир": {"kbgu": "высокожирные_свыше_30"},
            "millgri": {"name": "Millgri"},
        }
    
    def call_with_tools(self, system_prompt: str, user_query: str, tools: list) -> Optional[Dict[str, Any]]:
        """
        Имитирует вызов LLM с tool calling.
        
        Args:
            system_prompt: Системный промпт (игнорируется)
            user_query: Запрос пользователя
            tools: Список инструментов (игнорируется)
            
        Returns:
            Предопределенный ответ или None
        """
        logger.info(f"Mock LLM получил запрос: {user_query}")
        
        query_lower = user_query.lower()
        
        # Ищем совпадения в предопределенных ответах
        for key, params in self.responses.items():
            if key in query_lower:
                logger.info(f"Mock LLM выбрал параметры: {params}")
                return {
                    "tool_calls": [{
                        "function": {
                            "name": "filter_products",
                            "arguments": json.dumps(params)
                        }
                    }]
                }
        
        logger.info("Mock LLM не нашел подходящих инструментов")
        return None