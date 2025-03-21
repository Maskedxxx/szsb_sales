from typing import Set, List
import re

# Dictionary of stop words for Russian language
RUSSIAN_STOP_WORDS: Set[str] = {
    'а', 'без', 'более', 'бы', 'был', 'была', 'были', 'было', 'быть', 'в', 
    'вам', 'вас', 'весь', 'во', 'вот', 'все', 'всего', 'всех', 'вы', 'где', 
    'да', 'даже', 'для', 'до', 'его', 'ее', 'если', 'есть', 'ещё', 'же', 
    'за', 'здесь', 'и', 'из', 'или', 'им', 'их', 'к', 'как', 'ко', 'когда', 
    'кто', 'ли', 'либо', 'мне', 'может', 'мы', 'на', 'надо', 'наш', 'не', 
    'него', 'неё', 'нет', 'ни', 'них', 'но', 'ну', 'о', 'об', 'однако', 
    'он', 'она', 'они', 'оно', 'от', 'очень', 'по', 'под', 'при', 'с', 
    'со', 'так', 'также', 'такой', 'там', 'те', 'тем', 'то', 'того', 
    'тоже', 'той', 'только', 'том', 'ты', 'у', 'уже', 'хотя', 'чего', 
    'чей', 'чем', 'что', 'чтобы', 'чьё', 'чья', 'эта', 'эти', 'это', 
    'я', 'мне', 'мой', 'моя', 'моё', 'мои'
}

# Additional words specific to the beverages domain
DOMAIN_STOP_WORDS: Set[str] = {
    'мне', 'надо', 'нужно', 'хочу', 'есть', 'ли', 'пожалуйста',
    'скажите', 'подскажите', 'помогите', 'посоветуйте'
}

def clean_text(text: str) -> str:
    """
    Cleans text from stop words and other elements that don't carry semantic value.
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation and extra spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove stop words
    words = text.split()
    cleaned_words = [word for word in words if word not in RUSSIAN_STOP_WORDS 
                     and word not in DOMAIN_STOP_WORDS 
                     and len(word) > 1]  # Ignore single-character words
    
    # Assemble cleaned text
    cleaned_text = ' '.join(cleaned_words)
    
    return cleaned_text

def clean_utterances(utterances: List[str]) -> List[str]:
    """
    Cleans a list of examples from stop words.
    
    Args:
        utterances (List[str]): List of examples
        
    Returns:
        List[str]: List of cleaned examples
    """
    return [clean_text(utterance) for utterance in utterances]