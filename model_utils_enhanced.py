
from constants import LANGUAGES
from enhanced_examples import EXAMPLES_UPDATED, REGIONAL_PROMPTS, MULTILINGUAL_PROMPTS

def get_language_specific_examples(language_code=None):
    """
    Return language-specific examples based on the provided language code.
    
    Args:
        language_code: The language code to find examples for
        
    Returns:
        Dictionary with appropriate examples for the language
    """
    if not language_code:
        return EXAMPLES_UPDATED  # Return all examples if no language specified
        
    # Filter examples based on language
    filtered_examples = {}
    
    # Find examples that match the language script or are about that language
    for category, examples in EXAMPLES_UPDATED.items():
        # Language detection removed; just return all examples for now
        filtered_examples[category] = examples
    
    # If we don't have enough examples, supplement with English examples
    # No language detection, so skip supplementing
    
    return filtered_examples

def get_regional_prompts_by_language(language_code=None):
    """
    Return regional prompts specific to the provided language.
    
    Args:
        language_code: The language code to find prompts for
        
    Returns:
        List of regional prompts in the specified language
    """
    if not language_code:
        return REGIONAL_PROMPTS  # Return all prompts if no language specified
        
    # Filter prompts based on language
    language_prompts = []
    
    # No language detection, so just return all prompts
    return REGIONAL_PROMPTS

def get_multilingual_prompts_by_language(language_code=None):
    """
    Return multilingual prompts specific to the provided language.
    
    Args:
        language_code: The language code to find prompts for
        
    Returns:
        Dictionary with prompts in the specified language by category
    """
    if not language_code:
        return MULTILINGUAL_PROMPTS  # Return all prompts if no language specified
        
    # Filter prompts based on language
    filtered_prompts = {}
    
    # No language detection, so just return all prompts
    return MULTILINGUAL_PROMPTS

def language_code_to_name(code):
    """Convert a language code to its full name"""
    for name, lang_code in LANGUAGES:
        if lang_code == code:
            return name.split(' ')[0]  # Return just the language name part
    return "Unknown"

def suggest_native_language_prompt(detected_language):
    """
    Suggest a prompt in the user's detected native language
    to encourage multilingual interaction
    
    Args:
        detected_language: The detected language code
    
    Returns:
        A suggested prompt in the detected language
    """
    language_prompts = {
        "hi": "आप मुझसे हिंदी में कोई भी प्रश्न पूछ सकते हैं।",
        "ta": "நீங்கள் தமிழில் என்னிடம் எந்த கேள்வியும் கேட்கலாம்.",
        "te": "మీరు తెలుగులో నన్ను ఏదైనా ప్రశ్నించవచ్చు.",
        "bn": "আপনি আমাকে বাংলায় যেকোনো প্রশ্ন জিজ্ঞাসা করতে পারেন।",
        "mr": "तुम्ही मला मराठीत कोणताही प्रश्न विचारू शकता.",
        "gu": "તમે મને ગુજરાતીમાં કોઈપણ પ્રશ્ન પૂછી શકો છો.",
        "hi-ro": "Aap mujhse Hindi me koi bhi prashn pooch sakte hain."
    }
    
    return language_prompts.get(detected_language, "You can ask me questions in your native language.")
