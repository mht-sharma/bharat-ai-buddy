"""
Module to handle user feedback for multilingual responses in Bharat AI Buddy
"""
import json
import os
from datetime import datetime

# File to store feedback data
FEEDBACK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback_data.json")

def initialize_feedback_store():
    """
    Initialize the feedback data store if it doesn't exist
    
    Returns:
        Boolean indicating if initialization was successful
    """
    if not os.path.exists(FEEDBACK_FILE):
        default_data = {
            "multilingual_feedback": [],
            "language_stats": {},
            "created_at": datetime.now().isoformat()
        }
        try:
            with open(FEEDBACK_FILE, 'w') as f:
                json.dump(default_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error initializing feedback store: {str(e)}")
            return False
    return True

def save_feedback(prompt, response, language, rating, comment=None):
    """
    Save user feedback about a multilingual response
    
    Args:
        prompt: The original user prompt
        response: The AI response that was rated
        language: The language of the interaction
        rating: User rating (1-5)
        comment: Optional user comment
        
    Returns:
        Boolean indicating if feedback was saved successfully
    """
    # Initialize if needed
    if not os.path.exists(FEEDBACK_FILE):
        if not initialize_feedback_store():
            return False
    
    try:
        # Load existing feedback data
        with open(FEEDBACK_FILE, 'r') as f:
            data = json.load(f)
        
        # Add new feedback
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response_excerpt": response[:500] + "..." if len(response) > 500 else response,
            "language": language,
            "rating": rating
        }
        
        if comment:
            feedback_entry["comment"] = comment
            
        data["multilingual_feedback"].append(feedback_entry)
        
        # Update language statistics
        if language not in data["language_stats"]:
            data["language_stats"][language] = {
                "count": 0,
                "avg_rating": 0,
                "ratings": {str(i): 0 for i in range(1, 6)}
            }
            
        # Update stats
        lang_stats = data["language_stats"][language]
        lang_stats["count"] += 1
        lang_stats["ratings"][str(rating)] += 1
        
        # Recalculate average
        total_ratings = sum(int(r) * count for r, count in lang_stats["ratings"].items())
        total_count = sum(count for count in lang_stats["ratings"].values())
        lang_stats["avg_rating"] = round(total_ratings / total_count, 2) if total_count > 0 else 0
        
        # Save updated data
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump(data, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Error saving feedback: {str(e)}")
        return False

def get_feedback_stats():
    """
    Get statistics about multilingual response feedback
    
    Returns:
        Dictionary with feedback statistics or None if error occurs
    """
    try:
        if not os.path.exists(FEEDBACK_FILE):
            if not initialize_feedback_store():
                return None
            return {"language_stats": {}, "total_feedback": 0}
        
        with open(FEEDBACK_FILE, 'r') as f:
            data = json.load(f)
            
        stats = {
            "language_stats": data["language_stats"],
            "total_feedback": len(data["multilingual_feedback"]),
            "recent_feedback": data["multilingual_feedback"][-5:] if data["multilingual_feedback"] else []
        }
        
        return stats
    except Exception as e:
        print(f"Error getting feedback stats: {str(e)}")
        return None
