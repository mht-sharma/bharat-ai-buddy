# Updated examples for Bharat AI Buddy
# These examples showcase Sarvam-M's multilingual capabilities

EXAMPLES_UPDATED = {
    "Math/Logic": [
        "Solve: 234 + 567 in Hindi",
        "क्या 15 और 25 का LCM बता सकते हैं?",  # Direct Hindi input: Can you tell the LCM of 15 and 25?
        "ஒரு வட்டத்தின் பரப்பளவை எவ்வாறு கணக்கிடுவது?",  # Direct Tamil input: How to calculate the area of a circle?
        "त्रिकोण का क्षेत्रफल कैसे निकालें?",  # Direct Hindi: How to find the area of a triangle?
        "બેસેલ નંબર શું છે?"  # Direct Gujarati: What are Bessel numbers?
    ],
    "Code": [
        "Write a Python function to check for palindrome.",
        "বাইনারি সার্চ অ্যালগরিদম কীভাবে কাজ করে?",  # Direct Bengali input: How does binary search algorithm work?
        "પાયથોનમાં લિસ્ટ અને ટપલ વચ્ચે શું તફાવત છે?",  # Direct Gujarati input: What's the difference between list and tuple in Python?
        "जावा में स्ट्रिंग कैसे रिवर्स करें?",  # Direct Hindi: How to reverse a string in Java?
        "நெட்வொர்க் பாதுகாப்பு நிரல் எழுதுவது எப்படி?"  # Direct Tamil: How to write a network security program?
    ],
    "Culture": [
        "Why is Diwali celebrated?",
        "महाराष्ट्रातील गणेश चतुर्थी उत्सवाचे महत्व काय आहे?",  # Direct Marathi input: What is the significance of Ganesh Chaturthi festival in Maharashtra?
        "తెలుగు సంస్కృతిలో బోనాల పండుగ ఎందుకు జరుపుకుంటారు?",  # Direct Telugu input: Why is Bonalu festival celebrated in Telugu culture?
        "ভারতে গুরু পূর্ণিমার ঐতিহাসিক গুরুত্ব কী?",  # Direct Bengali: What is the historical importance of Guru Purnima in India?
        "ગુજરાતનો નવરાત્રિ ઉત્સવ કેવી રીતે ઉજવાય છે?"  # Direct Gujarati: How is Navratri festival celebrated in Gujarat?
    ],
    "Regional": [
        "कोकण किनारपट्टी के बारे में बताओ",  # Direct Hindi: Tell me about the Konkan coast
        "தமிழ்நாட்டு கோயில் கட்டிடக்கலை பற்றி விவரிக்கவும்",  # Direct Tamil: Describe Tamil Nadu's temple architecture
        "দুর্গা পূজার তাৎপর্য কী?",  # Direct Bengali: What is the significance of Durga Puja?
        "ગુજરાતી ઢોકળા બનાવવાની રીત",  # Direct Gujarati: Method to make Gujarati Dhokla
        "राजस्थान के लोक संगीत के प्रमुख वाद्य यंत्र कौन से हैं?",  # Direct Hindi: What are the main musical instruments of Rajasthan's folk music?
        "కాకతీయుల చరిత్రలో కేశవ టెంపుల్ యొక్క ప్రాముఖ్యత ఏమిటి?",  # Direct Telugu: What is the importance of Keshava Temple in Kakatiya history?
        "महाराष्ट्रातील वारकरी संप्रदाय काय आहे?",  # Direct Marathi: What is the Warkari tradition of Maharashtra?
        "அசாமிய பிஹு நடன வகைகள் மற்றும் அதன் சிறப்பம்சங்கள்"  # Direct Tamil: Types of Assamese Bihu dance and its features
    ],
    "Education": [
        "UPSC परीक्षा की तैयारी कैसे करें?",  # Direct Hindi: How to prepare for UPSC exam?
        "வேதியியல் வாய்ப்பாடுகளை எளிதாக நினைவில் வைக்க என்ன செய்ய வேண்டும்?",  # Direct Tamil: How to easily memorize chemistry formulas?
        "भारतातील गणित शिक्षणाचा इतिहास",  # Direct Marathi: History of mathematics education in India
        "జీవ శాస్త్రంలో ప్రాక్టికల్ పరీక్షకు ఎలా సిద్ధం కావాలి?",  # Direct Telugu: How to prepare for biology practical exam?
        "বায়োইনফরমেটিক্স কী এবং এর অ্যাপ্লিকেশন গুলি কী কী?",  # Direct Bengali: What is bioinformatics and what are its applications?
        "કોમ્પ્યુટર સાયન્સમાં કૃત્રિમ બુદ્ધિમત્તાનો ઉપયોગ"  # Direct Gujarati: Use of artificial intelligence in computer science
    ]
}

# Additional regional topic prompts for better multilingual showcasing
REGIONAL_PROMPTS = [
    # Hindi - North Indian context
    "उत्तराखंड के कुमाऊनी लोक संगीत के बारे में बताइए",  # Tell me about Kumaoni folk music of Uttarakhand
    "राजस्थानी मीणाकारी कला का इतिहास और महत्व",  # History and importance of Rajasthani Meenakari art
    
    # Tamil - South Indian context
    "தமிழ் மருத்துவத்தில் சித்த மருத்துவ முறை பற்றி விளக்குங்கள்",  # Explain about Siddha medicine system in Tamil medicine
    "கேரளாவின் கதகளி நடன வடிவத்தின் பின்னணி",  # Background of Kerala's Kathakali dance form
    
    # Bengali - East Indian context
    "পশ্চিমবঙ্গের পাট শিল্পের ইতিহাস এবং বর্তমান অবস্থা",  # History and current state of jute industry in West Bengal
    "অসমিয়া বিহু উৎসবের সাংস্কৃতিক গুরুত্ব",  # Cultural significance of Assamese Bihu festival
    
    # Marathi - West Indian context
    "महाराष्ट्रातील वारली चित्रकलेचे सांस्कृतिक महत्त्व",  # Cultural significance of Warli painting in Maharashtra
    "गोव्यातील कोंकणी भाषेची वैशिष्ट्ये आणि इतिहास",  # Characteristics and history of Konkani language in Goa
    
    # Telugu - South Indian context
    "ఆంధ్రప్రదేశ్‌లోని కాళహస్తి చిత్రలేఖన కళ గురించి",  # About Kalamkari painting art in Andhra Pradesh
    "తెలంగాణలోని నిజాం కాల వాస్తుశిల్పం గురించి వివరించండి",  # Describe Nizam era architecture in Telangana
    
    # Gujarati - West Indian context
    "કચ્છના રણમાં મીઠાના ઉત્પાદનની પરંપરાગત પદ્ધતિઓ",  # Traditional methods of salt production in Rann of Kutch
    "ગુજરાતના પટોળા સાડીની વણાટ કળા વિશે માહિતી આપો"  # Provide information about the weaving art of Patola sarees in Gujarat
]

# Additional multilingual prompts for different categories
MULTILINGUAL_PROMPTS = {
    "Science": [
        "परमाणु विखंडन और संलयन में क्या अंतर है?",  # Hindi: What's the difference between nuclear fission and fusion?
        "சூரிய குடும்பத்தின் கிரகங்களைப் பற்றிய தகவல்களை விவரிக்கவும்",  # Tamil: Describe information about the planets in the solar system
        "জৈব বিবর্তনের মূল নীতিগুলি কী কী?",  # Bengali: What are the basic principles of organic evolution?
        "ધ્વનિ તરંગો અને તેનું વિજ્ઞાન સમજાવો"  # Gujarati: Explain sound waves and their science
    ],
    "Technology": [
        "आर्टिफिशियल इंटेलिजेंस का भविष्य कैसा दिखता है?",  # Hindi: How does the future of artificial intelligence look?
        "ब्लॉकचेन तंत्रज्ञान कसे कार्य करते?",  # Marathi: How does blockchain technology work?
        "క్వాంటమ్ కంప్యూటింగ్ ప్రాథమిక సిద్ధాంతాలు ఏమిటి?",  # Telugu: What are the basic principles of quantum computing?
        "ডিপ লার্নিং এবং মেশিন লার্নিং এর মধ্যে পার্থক্য কী?"  # Bengali: What is the difference between deep learning and machine learning?
    ],
    "Arts": [
        "संगीत में तीनताल और एकताल के बीच अंतर क्या है?",  # Hindi: What's the difference between Teentaal and Ektaal in music?
        "தமிழ் இலக்கியத்தில் சங்க காலத்தின் முக்கியத்துவம் என்ன?",  # Tamil: What is the importance of Sangam period in Tamil literature?
        "कोणत्या घटकांमुळे कलाकृती 'शास्त्रीय' म्हणून ओळखली जाते?",  # Marathi: What factors make an artwork recognized as 'classical'?
        "ગુજરાતી સાહિત્યમાં મધ્યકાલીન યુગના મુખ્ય કવિઓ કોણ હતા?"  # Gujarati: Who were the main poets of the medieval period in Gujarati literature?
    ]
}
