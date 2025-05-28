"""
Language handling utilities for Bharat AI Buddy
"""
from typing import Optional, Tuple

# Complete list of supported languages with their codes
SUPPORTED_LANGUAGES = {
    # Formal scripts
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil", 
    "te": "Telugu",
    "gu": "Gujarati",
    "mr": "Marathi",
    "kn": "Kannada",
    "ml": "Malayalam",
    "or": "Oriya",
    "pa": "Punjabi",
    # Romanized versions
    "hi-ro": "Romanized Hindi",
    "bn-ro": "Romanized Bengali",
    "ta-ro": "Romanized Tamil",
    "te-ro": "Romanized Telugu",
    "gu-ro": "Romanized Gujarati",
    "mr-ro": "Romanized Marathi",
    "kn-ro": "Romanized Kannada",
    "ml-ro": "Romanized Malayalam",
    "or-ro": "Romanized Oriya",
    "pa-ro": "Romanized Punjabi",
    # Default
    "en": "English"
}

def process_query_language_neutral(query: str, system_prompt_template: str) -> Tuple[str, Optional[str]]:
    """
    Process a query with language-neutral system prompt
    
    Args:
        query: User's query in any language
        system_prompt_template: Template for system prompt
    
    Returns:
        Tuple of (final_prompt, detected_language)
        The language is detected but not used to modify the query
        It's returned only for analytics purposes
    """
    # Language detection is optional for analytics only
    # We don't need it for processing the query
    detected_language = None
    
    # For analytics purposes only (optional)
    # Language detection removed; just construct the prompt
    full_prompt = system_prompt_template.format(prompt=query)
    return full_prompt, None


def get_language_specific_hint(detected_language: Optional[str]) -> str:
    """
    Get a language-specific hint to show users
    
    Args:
        detected_language: Detected language code or None
    
    Returns:
        A hint string for users
    """
    if not detected_language or detected_language == "en":
        return "💡 Try asking your question directly in any Indian language - Sarvam-M understands them natively!"
    
    language_name = SUPPORTED_LANGUAGES.get(detected_language, "the detected language")
    
    if detected_language.endswith("-ro"):
        return f"💡 Detected {language_name}. You can also try using the native script for better results."
    else:
        return f"💡 Great! You're asking in {language_name}. Sarvam-M is optimized for Indian languages."
