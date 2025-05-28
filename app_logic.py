# filepath: /Users/mohitsharma/Downloads/apce/app_logic.py
# app_logic.py
"""
App logic and event handlers for Bharat AI Buddy
"""
from model_utils import generate_response
from quiz import generate_quiz_question, check_quiz_answer, quiz_state
from smolagents import ToolCallingAgent, WebSearchTool, CodeAgent, tool
from model_utils import sarvam_vllm
import requests
from markdownify import markdownify
from constants import SUBJECTS, LANGUAGES

# Import our enhanced custom tools
from agent_tools_improved import (
    visit_webpage, 
    search_wikipedia, 
    solve_math_problem,
    exam_question_generator, 
    analyze_code,
    explain_cultural_concept,
    check_exam_syllabus
)

sarvam_agent_model = sarvam_vllm

# Create specialized agents for different tasks
web_agent = ToolCallingAgent(
    tools=[WebSearchTool(), visit_webpage, search_wikipedia],
    model=sarvam_agent_model,
    max_steps=10,
    name="web_search_agent",
    description="Runs web searches and visits web pages for gathering information.",
)

math_agent = ToolCallingAgent(
    tools=[solve_math_problem, search_wikipedia],
    model=sarvam_agent_model,
    max_steps=8,
    name="math_logic_agent",
    description="Solves and explains mathematical and logical problems.",
)

code_agent = CodeAgent(
    tools=[analyze_code, WebSearchTool()],
    model=sarvam_agent_model,
    max_steps=12,
    name="coding_agent",
    description="Generates, analyzes and explains code.",
    stream_outputs=True,
    additional_authorized_imports=["math", "datetime", "random", "json", "re", "collections"]
)

exam_agent = ToolCallingAgent(
    tools=[exam_question_generator, check_exam_syllabus, search_wikipedia],
    model=sarvam_agent_model,
    max_steps=8,
    name="exam_agent",
    description="Helps with exam preparation and provides syllabus information.",
)

culture_agent = ToolCallingAgent(
    tools=[WebSearchTool(), visit_webpage, search_wikipedia, explain_cultural_concept],
    model=sarvam_agent_model,
    max_steps=10,
    name="culture_agent",
    description="Provides information about Indian culture, history, and current affairs.",
)

# Prompt templates for different types of questions
PROMPT_TEMPLATES = {
    "Math/Logic": (
        "You are Bharat AI Buddy, an advanced educational AI specializing in mathematics and logical reasoning for Indian academic contexts."
        "\n\nGuidelines for response:"
        "\n1. Structure your explanations with clear step-by-step methodology, utilizing numbered sequences for multi-step problems."
        "\n2. Employ standard mathematical notation with precise terminology while maintaining accessibility."
        "\n3. Present solutions that adhere to recognized educational frameworks and methodologies."
        "\n4. When responding to queries in Indian languages, maintain technical accuracy while preserving linguistic nuance."
        "\n5. For programming requests, deliver syntactically correct, well-structured Python code with comprehensive documentation."
        "\n6. When faced with ambiguous queries, request specific clarification before proceeding with analysis."
        "\n7. For inquiries outside mathematics or logical reasoning domains, respond: 'This query falls outside my specialized knowledge in mathematics and logical reasoning.'"
        "\n\nQuery for analysis: {prompt}"
    ),
    "Regional": (
        "You are Bharat AI Buddy powered by Sarvam, with deep expertise in India's regional cultures, languages, and traditions."
        "\n\nResponse guidelines:"
        "\n1. Showcase your deep understanding of regional Indian contexts, traditions, and cultural nuances."
        "\n2. Include authentic local terms and expressions when responding in the local language."
        "\n3. Mention region-specific variations and local contexts to demonstrate cultural awareness."
        "\n4. When responding in regional languages, maintain authentic phrasing while being accessible."
        "\n5. Incorporate relevant historical and cultural context specific to the region."
        "\n6. For traditional practices, include regional adaptations and modern relevance."
        "\n7. If writing in a native Indian script, include authentic and culturally significant terminology."
        "\n\nRegional query: {prompt}"
    ),
    "Code": (
        "You are Bharat AI Buddy, a professional software engineering consultant specializing in technical guidance for the Indian developer ecosystem."
        "\n\nImplementation guidelines:"
        "\n1. Generate enterprise-quality code with comprehensive documentation adhering to industry best practices."
        "\n2. Prioritize algorithmic efficiency and optimal resource utilization in all solutions."
        "\n3. Implement solutions utilizing native language constructs and standard libraries when appropriate."
        "\n4. Incorporate realistic, production-ready data models and implementation patterns."
        "\n5. For domain-specific languages, follow established conventions and patterns."
        "\n6. When addressing queries in Indian languages, maintain technical precision in your translated response."
        "\n7. For requests beyond software engineering domains, respond: 'This query extends beyond my specialized knowledge in software development and engineering.'"
        "\n\nDevelopment requirement: {prompt}"
    ),
    "Culture": (
        "You are Bharat AI Buddy, a cultural heritage specialist with expertise in Indian history, traditions, and contemporary societal developments."
        "\n\nConsultation parameters:"
        "\n1. Provide comprehensive, academically sound analysis on cultural topics with appropriate historical context."
        "\n2. For contemporary subjects, integrate verified information from authoritative sources with proper attribution."
        "\n3. When discussing cultural practices, include regional variations, historical evolution, and modern significance."
        "\n4. Present balanced perspectives that respect India's diverse cultural landscape."
        "\n5. Respond in the user's specified language while preserving cultural terminology and concepts."
        "\n6. For traditional events and practices, detail historical origins, regional adaptations, and contemporary observances."
        "\n7. For inquiries outside Indian cultural contexts, respond: 'This query falls outside my specialized knowledge of Indian cultural heritage and contemporary affairs.'"
        "\n\nCultural inquiry: {prompt}"
    ),
    "Exam": (
        "You are Bharat AI Buddy, an educational consultant specializing in Indian competitive examination preparation (UPSC, JEE, NEET, SSC, Bank PO, GATE, and related assessments)."
        "\n\nAcademic guidance protocol:"
        "\n1. Provide examination-focused responses aligned with official syllabi and established question patterns."
        "\n2. Structure answers with clear organization, emphasizing key concepts and examination focus areas."
        "\n3. Include relevant formulas, theorems, legal provisions, or principles central to the topic."
        "\n4. Integrate strategic examination techniques and methodological approaches where applicable."
        "\n5. Present information optimized for retention, utilizing appropriate formatting and concept mapping."
        "\n6. Respond in the specified language while maintaining technical precision and domain terminology."
        "\n7. For ambiguous queries, request examination-specific context before proceeding."
        "\n8. For inquiries outside competitive examination domains, respond: 'This query falls outside my specialized knowledge of Indian competitive examinations.'"
        "\n\nExamination query: {prompt}"
    ),
    "Default": (
        "You are Bharat AI Buddy, a comprehensive knowledge assistant calibrated for the Indian informational context."
        "\n\nResponse parameters:"
        "\n1. Provide factually accurate, well-structured information relevant to the query."
        "\n2. Respond in the user's specified language with appropriate cultural and contextual awareness."
        "\n3. For specialized inquiries, apply domain-appropriate methodologies and terminology."
        "\n4. If the user's query is in a native Indian language, respond in the same language."
        "\n5. For inquiries requiring specialized expertise beyond available knowledge domains, respond in the user's language: 'This query requires specialized expertise beyond my current knowledge framework.'"
        "\n\nUser inquiry: {prompt}"
    )
}

def get_prompt(tab, prompt, language=None):
    """
    Create a prompt template for the given tab and user query
    Designed to be language-neutral to leverage Sarvam-M's native multilingual capabilities
    
    Args:
        tab: The active tab in the UI
        prompt: The user's question or request
        language: Optional language preference (not required for Sarvam-M to process native language queries)
    
    Returns:
        A formatted prompt template
    """
    template = PROMPT_TEMPLATES.get(tab, PROMPT_TEMPLATES["Default"])
    
    # Language parameter is optional and doesn't affect Sarvam-M's ability to respond in native languages
    if language and "{language}" in template:
        return template.format(language=language, prompt=prompt)
    
    # Default case - just format with the prompt
    return template.format(prompt=prompt)

def app_fn(tab, prompt, mode, language, use_agents=True):
    """
    Main function to process user prompts based on tab context and user preferences.
    Uses specialized agents to augment the LLM's responses with additional context and capabilities.
    Leverages Sarvam-M's native support for Indian languages without requiring explicit language detection.
    
    Args:
        tab: The active tab (Math/Logic, Code, Culture, Exam)
        prompt: The user's question or request
        mode: "think" or "non-think" mode for response generation
        language: The user's preferred language from UI (optional, as model can handle direct native language input)
        use_agents: Whether to use specialized agents to augment responses
    """
    # Import language utilities if available, otherwise use standard approach
    try:
        from language_utils import process_query_language_neutral
        import logging
        logger = logging.getLogger("bharat_buddy")
        logger.info("Using language-neutral query processing")
    except ImportError:
        # Fallback to legacy approach with language detection
    # Use detailed prompt templates for each tab/type
    full_prompt = get_prompt(tab, prompt, language)
    
    # If agents are disabled, use standard text generation
    if not use_agents:
        reasoning, answer = generate_response(full_prompt, mode, language)
        if mode == "think" and reasoning:
            return f"🧠 Reasoning:\n{reasoning}\n\n✅ Answer:\n{answer}"
        else:
            return answer
    
    # Use agents to augment LLM responses when beneficial
    try:
        # Culture tab - augment LLM with cultural facts and context
        if tab == "Culture" or any(word in prompt.lower() for word in ["festival", "tradition", "history", "culture", "heritage"]):
            # For cultural topics, augment with factual information but let LLM generate the response
            factual_context = ""
            try:
                # Try to get factual context about the cultural concept
                cultural_search = prompt.replace("?", "").strip()
                context_result = explain_cultural_concept(cultural_search)
                
                if context_result and isinstance(context_result, str) and len(context_result) > 50:
                    factual_context = f"\n\nFactual context to incorporate into your response:\n{context_result}"
            except Exception as cultural_error:
                pass
            
            # For time-sensitive cultural queries, use web search to get current information
            if any(word in prompt.lower() for word in ["latest", "current", "news", "today", "recently", "trending"]):
                try:
                    web_results = web_agent.run(
                        f"Find the most recent and factual information about: {prompt}"
                    )
                    if web_results and len(web_results) > 100:
                        factual_context += f"\n\nRecent information to incorporate:\n{web_results[:1500]}"
                except:
                    pass
            
            # Let the LLM generate the answer with the additional factual context
            augmented_prompt = full_prompt + factual_context
            reasoning, answer = generate_response(augmented_prompt, mode, language)
            
            if mode == "think" and reasoning:
                return f"🧠 Reasoning:\n{reasoning}\n\n✅ Answer:\n{answer}"
            else:
                return answer
            
        # Math/Logic tab - augment LLM with computational search results
        elif tab == "Math/Logic" or any(word in prompt.lower() for word in ["solve", "equation", "calculate", "math", "problem", "formula"]):
            # For specific math problems, see if we can find additional resources
            if any(word in prompt.lower() for word in ["solve", "calculate", "find", "compute", "evaluate", "simplify"]):
                try:
                    # Try to get relevant math information
                    math_info = solve_math_problem(prompt)
                    
                    if math_info and len(math_info) > 20:
                        # Add the information to the LLM's prompt
                        augmented_prompt = f"{full_prompt}\n\nRelevant mathematical information:\n{math_info}"
                        reasoning, answer = generate_response(augmented_prompt, mode, language)
                        
                        if mode == "think" and reasoning:
                            return f"🧠 Reasoning:\n{reasoning}\n\n✅ Answer:\n{answer}"
                        else:
                            return answer
                except Exception as math_error:
                    # If math search fails, let the LLM handle it
                    pass
            
            # Let the LLM handle the math question (either initially or as fallback)
            reasoning, answer = generate_response(full_prompt, mode, language)
            if mode == "think" and reasoning:
                return f"🧠 Reasoning:\n{reasoning}\n\n✅ Answer:\n{answer}"
            else:
                return answer
            
        # Code tab - let LLM handle code analysis with augmentation from resources
        elif tab == "Code" or any(word in prompt.lower() for word in ["code", "function", "program", "algorithm", "class", "implement"]):
            # If the request specifically involves code analysis
            if "analyze" in prompt.lower() or "review" in prompt.lower() or "improve" in prompt.lower():
                try:
                    # Extract code block from the prompt if it exists
                    import re
                    code_block_match = re.search(r'```(?:\w+)?\s*\n([\s\S]+?)\n```', prompt)
                    
                    if code_block_match:
                        code_to_analyze = code_block_match.group(1)
                        # Determine language if possible
                        lang_match = re.search(r'```(\w+)', prompt)
                        language = lang_match.group(1) if lang_match else "python"
                        
                        # Get best practices resources
                        analysis_resources = analyze_code(code_to_analyze, language)
                        
                        if analysis_resources and isinstance(analysis_resources, dict):
                            # Create a readable summary of the resources
                            resources_text = ""
                            
                            if "dependencies" in analysis_resources:
                                resources_text += f"Dependencies detected: {', '.join(analysis_resources['dependencies'])}\n\n"
                            
                            if "notes" in analysis_resources:
                                resources_text += f"Notes: {' '.join(analysis_resources['notes'])}\n\n"
                                
                            if "resources" in analysis_resources:
                                resources_text += f"Relevant best practices resources:\n- " + "\n- ".join(analysis_resources["resources"])
                            
                            if resources_text:
                                # Augment the LLM prompt with these resources
                                augmented_prompt = f"{full_prompt}\n\nCode information and resources:\n{resources_text}"
                                reasoning, answer = generate_response(augmented_prompt, mode, language)
                                
                                if mode == "think" and reasoning:
                                    return f"🧠 Reasoning:\n{reasoning}\n\n✅ Answer:\n{answer}"
                                else:
                                    return answer
                except Exception as analysis_error:
                    # If analysis fails, let the LLM handle it
                    pass
            
            # For code generation, still use the CodeAgent as it's particularly valuable
            try:
                code_response = code_agent.run(full_prompt)
                if code_response and isinstance(code_response, str):
                    return code_response.strip()
            except Exception as code_error:
                # Fallback to LLM if the agent fails
                pass
                
            # Fallback to standard LLM
            reasoning, answer = generate_response(full_prompt, mode, language)
            if mode == "think" and reasoning:
                return f"🧠 Reasoning:\n{reasoning}\n\n✅ Answer:\n{answer}"
            else:
                return answer
            
        # Exam tab - augment LLM with syllabus information
        elif tab == "Exam":
            extra_context = ""
            
            # For syllabus-related queries, augment with syllabus information
            if any(word in prompt.lower() for word in ["syllabus", "curriculum", "topics", "pattern", "preparation"]):
                try:
                    # Extract the exam type from the prompt if possible
                    from constants import EXAMS
                    exam_type = None
                    for exam in EXAMS:
                        if exam.lower() in prompt.lower():
                            exam_type = exam
                            break
                    
                    if exam_type:
                        # Get syllabus information to augment the response
                        subject = None
                        for subject_candidate in SUBJECTS.get(exam_type, []):
                            if subject_candidate.lower() in prompt.lower():
                                subject = subject_candidate
                                break
                        
                        syllabus_info = check_exam_syllabus(exam_type, subject)
                        if syllabus_info and len(syllabus_info) > 50:
                            extra_context += f"\n\nSyllabus reference information:\n{syllabus_info}"
                except:
                    pass
            
            # For exam preparation questions, get study materials information
            if any(word in prompt.lower() for word in ["books", "reference", "material", "resources", "study"]):
                try:
                    # Get recommended study resources
                    from smolagents import WebSearchTool
                    web_tool = WebSearchTool()
                    search_query = f"recommended books reference materials for {prompt}"
                    search_results = web_tool(search_query)
                    
                    if search_results and len(search_results) > 100:
                        # Extract only the most relevant portions mentioning books or references
                        import re
                        resource_mentions = re.findall(r'([^.!?]*(?:book|reference|material|resource)[^.!?]*[.!?])', search_results, re.IGNORECASE)
                        if resource_mentions:
                            resources_text = " ".join(resource_mentions[:5])  # Limit to first 5 mentions
                            extra_context += f"\n\nReference materials:\n{resources_text}"
                except:
                    pass
            
            # For question generation, augment with contextual information
            if "generate" in prompt.lower() and ("question" in prompt.lower() or "mock" in prompt.lower()):
                try:
                    # Extract the exam type and subject from the prompt
                    from constants import EXAMS
                    exam_type = None
                    subject = None
                    
                    for exam in EXAMS:
                        if exam.lower() in prompt.lower():
                            exam_type = exam
                            break
                    
                    if exam_type:
                        for subject_candidate in SUBJECTS.get(exam_type, []):
                            if subject_candidate.lower() in prompt.lower():
                                subject = subject_candidate
                                break
                        
                        if subject:
                            # Get contextual information for generating questions
                            question_context = exam_question_generator(exam_type, subject)
                            if question_context and len(question_context) > 50:
                                extra_context += f"\n\nQuestion generation context:\n{question_context}"
                except:
                    pass
            
            # Let the LLM generate a response with the additional context
            if extra_context:
                augmented_prompt = full_prompt + extra_context
                reasoning, answer = generate_response(augmented_prompt, mode, language)
                
                if mode == "think" and reasoning:
                    return f"🧠 Reasoning:\n{reasoning}\n\n✅ Answer:\n{answer}"
                else:
                    return answer
            else:
                # If no extra context, use standard generation
                reasoning, answer = generate_response(full_prompt, mode, language)
                if mode == "think" and reasoning:
                    return f"🧠 Reasoning:\n{reasoning}\n\n✅ Answer:\n{answer}"
                else:
                    return answer
            
        # Default: use standard text generation for anything else
        else:
            reasoning, answer = generate_response(full_prompt, mode, language)
            if mode == "think" and reasoning:
                return f"🧠 Reasoning:\n{reasoning}\n\n✅ Answer:\n{answer}"
            else:
                return answer
                
    except Exception as e:
        # Fallback to standard generation on agent errors
        try:
            reasoning, answer = generate_response(full_prompt, mode, language)
            if mode == "think" and reasoning:
                return f"🧠 Reasoning:\n{reasoning}\n\n✅ Answer:\n{answer}"
            else:
                return answer
        except:
            return f"Sorry, I encountered an error while processing your request: {str(e)}"

def example_click(tab, example, mode, language, use_agents=True):
    return app_fn(tab, example, mode, language, use_agents)

def trending_click(tab, trending, mode, language, use_agents=True):
    return app_fn(tab, trending, mode, language, use_agents)

def update_subjects(selected_exam):
    from gradio import Dropdown
    return Dropdown.update(choices=SUBJECTS[selected_exam], value=SUBJECTS[selected_exam][0])

def start_quiz_fn(exam, subject, language):
    question = generate_quiz_question(exam, subject, language)
    quiz_state["question"] = question
    import re
    match = re.search(r"Answer:\s*([A-Da-d])", question)
    quiz_state["correct"] = match.group(1).upper() if match else "A"
    return question, ""

def submit_answer_fn(user_ans):
    correct = quiz_state.get("correct", "A")
    if check_quiz_answer(user_ans, correct):
        return "✅ Correct!", ""
    else:
        return f"❌ Incorrect. Correct answer: {correct}", ""

def get_syllabus_info(exam, subject):
    """
    Get detailed syllabus information for a specific exam and subject.
    Uses check_exam_syllabus to retrieve factual information that augments the LLM's knowledge.
    
    Args:
        exam: The competitive exam name
        subject: The specific subject
        
    Returns:
        Detailed syllabus information with the LLM's interpretation
    """
    try:
        # First, get the factual syllabus information 
        syllabus_info = check_exam_syllabus(exam, subject)
        
        # Build a prompt that incorporates this information
        prompt = f"Provide a comprehensive overview of the syllabus for {subject} in {exam} examination. Include important topics, recommended approach to studying each topic, and focus areas."
        
        if syllabus_info and len(syllabus_info) > 50:
            prompt += f"\n\nIncorporate this factual syllabus information in your response:\n{syllabus_info}"
            
        # Have the LLM generate a response that incorporates the factual data
        reasoning, answer = generate_response(prompt, "non-think", "en")
        return answer
    except Exception as e:
        return f"Error retrieving syllabus: {str(e)}"

def get_study_tips(exam, subject):
    """
    Get study tips for a specific exam and subject
    
    Args:
        exam: The competitive exam name
        subject: The specific subject
        
    Returns:
        Study tips and strategies
    """
    try:
        # First, try to get some factual information about the exam pattern
        syllabus_info = check_exam_syllabus(exam, subject)
        
        # Build a prompt that incorporates this information
        prompt = f"Provide effective study strategies and tips for preparing {subject} for the {exam} examination. Include time management advice, important focus areas, and common mistakes to avoid."
        
        if syllabus_info and len(syllabus_info) > 50:
            prompt += f"\n\nIncorporate this exam information in your response:\n{syllabus_info}"
            
        # Have the LLM generate a response that incorporates the factual data
        reasoning, answer = generate_response(prompt, "non-think", "en")
        return answer
    except Exception as e:
        return f"Error generating study tips: {str(e)}"

def exam_qa(exam, subject, question, language):
    """
    Answer exam-related questions with factual augmentation
    
    Args:
        exam: The competitive exam name
        subject: The specific subject
        question: The user's question
        language: The preferred language
        
    Returns:
        Detailed answer to the question
    """
    try:
        # Get contextual information first
        context = ""
        
        # Try to get syllabus context if applicable
        if any(word in question.lower() for word in ["syllabus", "curriculum", "topics", "pattern"]):
            syllabus_info = check_exam_syllabus(exam, subject)
            if syllabus_info and len(syllabus_info) > 50:
                context += f"\n\nSyllabus information:\n{syllabus_info}"
        
        # For subject content questions, try to get factual information
        if not context:
            try:
                search_term = f"{exam} {subject} {question}"
                wiki_info = search_wikipedia(search_term)
                if wiki_info and len(wiki_info) > 100:
                    context += f"\n\nFactual information:\n{wiki_info}"
            except:
                pass
                
        # Create augmented prompt
        full_prompt = f"As an expert in {exam} preparation, specifically for the subject {subject}, answer the following question in {language}: {question}"
        
        if context:
            full_prompt += f"\n\nIncorporate this factual information in your response:{context}"
        
        # Generate response
        reasoning, answer = generate_response(full_prompt, "non-think", language)
        return answer
    except Exception as e:
        return f"Error processing your question: {str(e)}"
        
def generate_regional_query(region: str, state: str, topic: str, language: str, prompt: str = "") -> str:
    """
    Generates a response for a query about a specific Indian state and regional topic,
    showcasing Sarvam's deep understanding of regional nuances.
    
    Args:
        region: The region of India (North, South, East, West)
        state: The specific state within the region
        topic: The topic of interest (cuisine, festivals, etc.)
        language: The language for the response
        prompt: Optional additional query details
        
    Returns:
        A detailed response about the regional topic
    """
    try:
        # First, search for regional information
        search_query = f"{state} {topic.lower()}"
        context = ""
        
        try:
            # Try Wikipedia for factual information
            wiki_info = search_wikipedia(search_query)
            if wiki_info and len(wiki_info) > 100:
                context += f"\n\nFactual information about {state} {topic.lower()}:\n{wiki_info}"
        except:
            pass
            
        # If Wikipedia didn't return much or any information, try web search
        if not context or len(context) < 200:
            try:
                from smolagents import WebSearchTool
                web_tool = WebSearchTool()
                web_results = web_tool(f"{state} {topic.lower()} India authentic traditional")
                
                if web_results and len(web_results) > 100:
                    context += f"\n\nAdditional information from web search:\n{web_results[:1500]}"
            except:
                pass
        
        # Generate a prompt that showcases Sarvam's regional expertise
        language_code = "en"
        for lang_name, code in LANGUAGES:
            if lang_name == language:
                language_code = code
                break
        
        # Build a prompt that will highlight multilingual capabilities
        query = prompt if prompt else f"Explain {topic.lower()} of {state}"
        
        multilingual_prompt = (
            f"You are Sarvam, an AI assistant with deep expertise in Indian regional cultures and languages. "
            f"Provide a rich, detailed explanation about the {topic.lower()} of {state} in {language}. "
            f"Incorporate authentic local terms, traditions, and contexts. "
            f"If responding in an Indian language other than English, incorporate some authentic local terms "
            f"from that region while keeping the overall text understandable. "
            f"\n\nQuery: {query}"
        )
        
        # Add the factual context if we have it
        if context:
            multilingual_prompt += f"\n\nIncorporate these facts in your response:{context}"
            
        # Generate response - we'll show both thinking and final answer for transparency
        reasoning, answer = generate_response(multilingual_prompt, "think", language_code)
        
        response = ""
        if reasoning:
            response += f"🧠 Sarvam is analyzing regional information about {state}:\n{reasoning}\n\n"
            
        response += f"✅ **{state} {topic}**\n\n{answer}"
        
        # Include a note about Sarvam's capabilities
        note = f"\n\n---\n*This response showcases Sarvam's understanding of Indian regional contexts and multilingual capabilities.*"
        
        return response + note
        
    except Exception as e:
        return f"Error generating regional information: {str(e)}"
