# All static data and constants for the app

LANGUAGES = [
    ("English", "en"),
    ("Hindi (हिन्दी)", "hi"),
    ("Tamil (தமிழ்)", "ta"),
    ("Telugu (తెలుగు)", "te"),
    ("Bengali (বাংলা)", "bn"),
    ("Marathi (मराठी)", "mr"),
    ("Gujarati (ગુજરાતી)", "gu"),
    ("Kannada (ಕನ್ನಡ)", "kn"),
    ("Malayalam (മലയാളം)", "ml"),
    ("Oriya (ଓଡ଼ିଆ)", "or"),
    ("Punjabi (ਪੰਜਾਬੀ)", "pa"),
    ("Romanized Hindi", "hi-ro"),
    ("Romanized Tamil", "ta-ro"),
    ("Romanized Telugu", "te-ro"),
    ("Romanized Bengali", "bn-ro"),
    ("Romanized Marathi", "mr-ro"),
    ("Romanized Gujarati", "gu-ro"),
]

EXAMPLES = {
    "Math/Logic": [
        "Solve: 234 + 567 in Hindi",
        "क्या 15 और 25 का LCM बता सकते हैं?",  # Direct Hindi input: Can you tell the LCM of 15 and 25?
        "ஒரு வட்டத்தின் பரப்பளவை எவ்வாறு கணக்கிடுவது?"  # Direct Tamil input: How to calculate the area of a circle?
    ],
    "Code": [
        "Write a Python function to check for palindrome.",
        "বাइনারি সার্চ অ্যালগরিদম কীভাবে কাজ করে?",  # Direct Bengali input: How does binary search algorithm work?
        "પાયથોનમાં લિસ્ટ અને ટપલ વચ્ચે શું તફાવત છે?"  # Direct Gujarati input: What's the difference between list and tuple in Python?
    ],
    "Culture": [
        "Why is Diwali celebrated?",
        "महाराष्ट्रातील गणेश चतुर्थी उत्सवाचे महत्व काय आहे?",  # Direct Marathi input: What is the significance of Ganesh Chaturthi festival in Maharashtra?
        "తెలుగు సంస్కృతిలో బోనాల పండుగ ఎందుకు జరుపుకుంటారు?"  # Direct Telugu input: Why is Bonalu festival celebrated in Telugu culture?
    ],
    "Regional": [
        "कोकण किनारपट्टी के बारे में बताओ",  # Direct Hindi: Tell me about the Konkan coast
        "தமிழ்நாட்டு கோயில் கட்டிடக்கலை பற்றி விவரிக்கவும்",  # Direct Tamil: Describe Tamil Nadu's temple architecture
        "দুর্গা পূজার তাৎপর্য কী?",  # Direct Bengali: What is the significance of Durga Puja?
        "ગુજરાતી ઢોકળા બનાવવાની રીત"  # Direct Gujarati: Method to make Gujarati Dhokla
    ]
}

TRENDING = [
    "What is Chandrayaan-3?",
    "Who is the current Prime Minister of India?",
    "Solve: 1234 x 5678",
    "Write a Python program for Fibonacci series."
]

# Regional contexts to showcase Sarvam's understanding of diverse Indian regions
REGIONS = {
    "North India": ["Delhi", "Uttar Pradesh", "Himachal Pradesh", "Punjab", "Haryana"],
    "South India": ["Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh", "Telangana"],
    "East India": ["West Bengal", "Odisha", "Bihar", "Assam", "Jharkhand"],
    "West India": ["Maharashtra", "Gujarat", "Rajasthan", "Goa"]
}

# Regional topics to showcase multilingual capabilities
REGIONAL_TOPICS = {
    "Cuisines": "Traditional foods and cooking techniques specific to regions",
    "Festivals": "Local celebrations and their significance",
    "Art Forms": "Traditional arts, crafts, dance, and music",
    "History": "Regional historical events and personalities",
    "Languages": "Linguistic features and dialects",
    "Folk Tales": "Traditional stories and legends passed through generations",
    "Clothing": "Traditional attire and textiles of the region",
    "Architecture": "Distinctive building styles and monuments",
    "Literature": "Regional literary traditions, famous works and authors",
    "Music": "Traditional and contemporary musical forms and instruments",
    "Dance Forms": "Classical and folk dance traditions unique to regions",
    "Handicrafts": "Traditional crafts, techniques and their cultural significance",
    "Rituals": "Cultural and religious ceremonies and practices",
    "Medicines": "Traditional medicinal practices and herbal remedies"
}

EXAMS = [
    "UPSC",
    "JEE",
    "NEET",
    "SSC",
    "Bank PO",
    "GATE"
]

SUBJECTS = {
    "UPSC": ["History", "Geography", "Politics", "Economics", "Indian Culture", "Current Affairs", "Environment & Ecology"],
    "JEE": ["Maths", "Physics", "Chemistry", "Coordinate Geometry", "Calculus", "Modern Physics", "Organic Chemistry"],
    "NEET": ["Biology", "Physics", "Chemistry", "Human Physiology", "Cell Biology", "Genetics", "Thermodynamics"],
    "SSC": ["General Awareness", "Reasoning", "Quantitative Aptitude", "English Comprehension", "General Science"],
    "Bank PO": ["Reasoning", "Quantitative Aptitude", "English", "Computer Awareness", "Banking Awareness", "Financial Management"],
    "GATE": ["Computer Science", "Electronics", "Mechanical", "Civil", "Electrical", "Data Structures & Algorithms", "Operating Systems"]
}
