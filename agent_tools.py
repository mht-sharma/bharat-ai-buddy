"""
Custom tools for Bharat AI Buddy using smolagents capabilities
"""
from smolagents import tool, Tool
import requests
import wikipedia
from markdownify import markdownify
import json
from typing import Optional, List, Dict, Any
import re
import logging

logger = logging.getLogger("bharat_buddy")

@tool
def visit_webpage(url: str) -> str:
    """Gets the content from a webpage.
    
    Args:
        url: The URL of the webpage to visit.
    
    Returns:
        The content of the webpage in markdown format.
    """
    logger.info(f"visit_webpage called with url: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = markdownify(response.text)
        logger.info(f"Successfully fetched webpage content from {url}")
        return content
    except Exception as e:
        logger.error(f"Error in visit_webpage: {e}")
        return f"Error: {e}"

@tool
def search_wikipedia(query: str, language: str = "en") -> str:
    """Searches Wikipedia for information.
    
    Args:
        query: The search query.
        language: The Wikipedia language code (default: "en" for English)
    
    Returns:
        A summary of the information found.
    """
    logger.info(f"search_wikipedia called with query: {query}, language: {language}")
    try:
        # Set the language
        wikipedia.set_lang(language)
        
        # Search for pages
        search_results = wikipedia.search(query, results=5)
        logger.info(f"Wikipedia search results: {search_results}")
        
        if not search_results:
            return f"No Wikipedia articles found for '{query}'."
        
        # Try to get a summary for the first result
        try:
            page = wikipedia.page(search_results[0], auto_suggest=False)
            summary = page.summary
            url = page.url
            logger.info(f"Found Wikipedia page: {page.title}")
            return f"## {page.title}\n\n{summary}\n\nSource: {url}"
        except wikipedia.DisambiguationError as e:
            # If disambiguation page, pick the first option
            try:
                page = wikipedia.page(e.options[0], auto_suggest=False)
                summary = page.summary
                url = page.url
                logger.info(f"Disambiguation resolved to: {page.title}")
                return f"## {page.title}\n\n{summary}\n\nSource: {url}"
            except Exception as de:
                logger.error(f"Error resolving disambiguation: {de}")
                return f"Multiple Wikipedia articles found for '{query}'. Options include: {', '.join(e.options[:5])}."
        except Exception as e:
            logger.error(f"Error retrieving Wikipedia page: {e}")
            return f"Error retrieving Wikipedia page for '{query}': {e}"
    except Exception as e:
        logger.error(f"Error searching Wikipedia: {e}")
        return f"Error searching Wikipedia: {e}"

@tool
def solve_math_problem(problem: str) -> str:
    """Provides computational assistance for math problems to augment LLM explanations.
    This tool performs basic calculations without replacing the LLM's conceptual understanding.
    
    Args:
        problem: The mathematical problem to solve.
    
    Returns:
        Computational results to supplement the LLM's mathematical explanation.
    """
    logger.info(f"solve_math_problem called with problem: {problem}")
    try:
        # Try to find relevant online information about the math problem
        from smolagents import WebSearchTool
        search_tool = WebSearchTool()
        
        # Extract key math terms from the problem
        math_terms = re.findall(r'(equation|solve|integrate|derivative|calculus|algebra|geometry|trigonometry|differentiate|simplify|factor)', problem.lower())
        logger.info(f"Extracted math terms: {math_terms}")
        
        search_results = ""
        if math_terms:
            search_query = f"{problem} solution method mathematical"
            try:
                search_results = search_tool(search_query)
                logger.info(f"Search results for math problem: {search_results}")
                
                # Extract the most relevant part of the search results
                if search_results and len(search_results) > 100:
                    # Find sentences that contain mathematical notation or terms
                    sentences = re.split(r'[.!?]', search_results)
                    relevant_sentences = []
                    
                    for sentence in sentences:
                        # Look for mathematical notation, numbers, or key terms
                        if (re.search(r'[+\-*/^=]|\d+', sentence) and 
                            any(term in sentence.lower() for term in ['formula', 'equation', 'solution', 'calculate', 'solve'])):
                            relevant_sentences.append(sentence.strip())
                    
                    if relevant_sentences:
                        search_results = "Relevant mathematical approaches:\n- " + "\n- ".join(relevant_sentences[:3])
                        logger.info(f"Relevant mathematical approaches found: {relevant_sentences[:3]}")
                    else:
                        search_results = ""
            except Exception as se:
                logger.error(f"Error in math problem search: {se}")
                search_results = ""
        
        # Try basic computation for simple arithmetic expressions
        try:
            # Check if problem contains a clear arithmetic expression
            arithmetic_match = re.search(r'(\d+\s*[\+\-\*/]\s*\d+(?:\s*[\+\-\*/]\s*\d+)*)', problem)
            if arithmetic_match:
                expression = arithmetic_match.group(1).replace(' ', '')
                # Safely evaluate the expression
                result = eval(expression)
                calculation = f"Arithmetic calculation: {expression} = {result}"
                logger.info(f"Performed arithmetic calculation: {calculation}")
                
                if search_results:
                    return f"{search_results}\n\n{calculation}"
                else:
                    return calculation
        except Exception as ae:
            logger.error(f"Error in arithmetic calculation: {ae}")
            # If simple arithmetic fails, just return the search results
            if search_results:
                return search_results
            
        # If we couldn't find helpful information, let the LLM handle it
        return "Unable to find specific computational assistance for this math problem. The LLM can solve this based on its mathematical knowledge."
        
    except Exception as e:
        logger.error(f"Error retrieving computational assistance: {e}")
        return "Error retrieving computational assistance. The LLM can solve this math problem using its built-in knowledge."

@tool
def exam_question_generator(exam_type: str, subject: str, difficulty: str = "medium") -> str:
    """Generates relevant context to help the LLM create an exam question.
    
    Args:
        exam_type: The type of exam (e.g., "UPSC", "JEE", "NEET").
        subject: The subject of the question.
        difficulty: The difficulty level (easy, medium, hard).
    
    Returns:
        Contextual information to help generate a relevant exam question.
    """
    logger.info(f"exam_question_generator called with exam_type: {exam_type}, subject: {subject}, difficulty: {difficulty}")
    try:
        # Build a rich context for the LLM to use when generating questions
        context_sections = []
        
        # First, search for topic information in Wikipedia
        try:
            wikipedia.set_lang("en")
            search_results = wikipedia.search(f"{exam_type} {subject}", results=3)
            logger.info(f"Wikipedia search results for exam question generation: {search_results}")
            
            if search_results:
                try:
                    # Get exam-related information
                    exam_page = None
                    for result in search_results:
                        if exam_type.lower() in result.lower():
                            exam_page = wikipedia.page(result, auto_suggest=False)
                            break
                    
                    if exam_page:
                        # Extract exam format information
                        format_info = ""
                        content = exam_page.content.lower()
                        
                        # Try to extract question format information
                        if "question" in content and "format" in content:
                            sections = exam_page.content.split('\n== ')
                            for section in sections:
                                if "question" in section.lower() or "format" in section.lower() or "pattern" in section.lower():
                                    format_info = section[:300] + "..."
                                    break
                        
                        if format_info:
                            context_sections.append(f"Exam format information:\n{format_info}")
                            logger.info(f"Extracted exam format information: {format_info}")
                    
                    # Get subject-related information
                    subject_page = None
                    subject_results = wikipedia.search(f"{subject} {exam_type}", results=3)
                    if subject_results:
                        subject_page = wikipedia.page(subject_results[0], auto_suggest=False)
                        
                        # Extract a short summary about the subject
                        if subject_page:
                            subject_info = subject_page.summary[:300] + "..."
                            context_sections.append(f"Subject information:\n{subject_info}")
                            logger.info(f"Extracted subject information: {subject_info}")
                            
                            # Try to extract key topics in the subject
                            key_topics = []
                            content = subject_page.content
                            topic_matches = re.findall(r'\n== ([^=]+) ==', content)
                            if topic_matches:
                                key_topics = topic_matches[:5]
                                context_sections.append(f"Key topics in {subject}:\n- " + "\n- ".join(key_topics))
                                logger.info(f"Extracted key topics: {key_topics}")
                
                    except Exception as wiki_error:
                        logger.error(f"Error in Wikipedia information extraction: {wiki_error}")
                        pass
            
            # If we couldn't get specific information, provide general guidance
            if not context_sections:
                if exam_type.lower() == "upsc":
                    context_sections.append(f"UPSC questions in {subject} typically test conceptual understanding and application of knowledge.")
                elif exam_type.lower() == "jee":
                    context_sections.append(f"JEE questions in {subject} typically require strong problem-solving skills and analytical thinking.")
                elif exam_type.lower() == "neet":
                    context_sections.append(f"NEET questions in {subject} focus on testing understanding of fundamental concepts in life sciences.")
            
            # Add difficulty-specific guidance
            if difficulty.lower() == "easy":
                context_sections.append(f"For an easy {subject} question, focus on basic definitions, straightforward applications, or simple calculations.")
            elif difficulty.lower() == "medium":
                context_sections.append(f"For a medium difficulty {subject} question, introduce multi-step problems or conceptual applications.")
            elif difficulty.lower() == "hard":
                context_sections.append(f"For a difficult {subject} question, combine multiple concepts, require deeper analysis, or use uncommon scenarios.")
            
            # Combine all the context sections
            full_context = "\n\n".join(context_sections)
            logger.info(f"Generated context for exam question: {full_context}")
            
            return f"Context for generating a {difficulty}-level {subject} question for {exam_type}:\n\n{full_context}"
            
        except Exception as e:
            logger.error(f"Error generating exam question context: {e}")
            return f"The LLM should generate a {difficulty}-level {subject} question for {exam_type} based on its knowledge of typical exam patterns."
    
    except Exception as e:
        logger.error(f"Error in exam_question_generator: {e}")
        return f"Error retrieving exam context. The LLM can generate a question based on its knowledge of typical {exam_type} exam patterns."

@tool
def analyze_code(code: str, language: str = "python") -> Dict[str, Any]:
    """Searches for code quality resources to augment LLM code analysis.
    This tool provides relevant online resources about code best practices rather than
    performing detailed analysis that the LLM can handle.
    
    Args:
        code: The code to analyze.
        language: The programming language of the code.
    
    Returns:
        Basic information and relevant resources to help the LLM analyze the code.
    """
    logger.info(f"analyze_code called for {language} code analysis")
    result = {
        "language": language,
        "code_length": len(code),
        "line_count": len(code.split('\n')),
        "resources": [],
        "notes": []
    }
    
    try:
        # Get basic information about the code
        
        # Identify imports or dependencies
        dependencies = []
        
        if language.lower() == "python":
            # Find Python imports
            import_pattern = re.compile(r'^import\s+(\w+)|^from\s+(\w+)', re.MULTILINE)
            matches = import_pattern.findall(code)
            for match in matches:
                if match[0]:  # import x
                    dependencies.append(match[0])
                elif match[1]:  # from x import y
                    dependencies.append(match[1])
        
        elif language.lower() in ["javascript", "js", "typescript", "ts"]:
            # Find JS/TS imports and requires
            import_pattern = re.compile(r'(import|require)\s*\(?[\'"]([^\'"]*)[\'"]\)?', re.MULTILINE)
            matches = import_pattern.findall(code)
            for match in matches:
                if match[1]:
                    dependencies.append(match[1])
        
        # Add relevant dependencies to the result if found
        if dependencies:
            result["dependencies"] = list(set(dependencies))[:10]  # Limit to 10 unique dependencies
            logger.info(f"Identified dependencies: {result['dependencies']}")
        
        # Check for critical security patterns that should be flagged
        security_patterns = {
            "python": [r'eval\(', r'exec\(', r'os\.system\(', r'subprocess\.call\(', r'pickle\.loads\('],
            "javascript": [r'eval\(', r'document\.write\(', r'\.innerHTML\s*=', r'new Function\('],
            "typescript": [r'eval\(', r'document\.write\(', r'\.innerHTML\s*=', r'new Function\('],
        }
        
        lang_key = language.lower()
        if lang_key not in security_patterns:
            lang_key = "python"  # default
            
        for pattern in security_patterns.get(lang_key, []):
            if re.search(pattern, code):
                result["notes"].append(f"Found potentially unsafe pattern: {pattern}")
                logger.warning(f"Unsafe pattern detected in code: {pattern}")
        
        # Search for best practices resources online based on the language
        from smolagents import WebSearchTool
        search_tool = WebSearchTool()
        
        try:
            search_query = f"{language} programming best practices code quality standards"
            search_results = search_tool(search_query)
            logger.info(f"Search results for code analysis: {search_results}")
            
            # Extract useful resources from search results
            if search_results:
                # Look for links to documentation or guides
                url_pattern = re.compile(r'(https?://[^\s]+(?:\.org|\.com|\.io|\.dev)/[^\s]+)')
                urls = url_pattern.findall(search_results)
                
                if urls:
                    # Add only relevant URLs that contain keywords related to code quality
                    relevant_urls = []
                    quality_terms = ['best practices', 'style guide', 'lint', 'quality', 'standards', 'convention']
                    
                    for url in urls[:5]:  # Limit to first 5 URLs
                        if any(term in url.lower() for term in quality_terms):
                            relevant_urls.append(url)
                    
                    if relevant_urls:
                        result["resources"] = relevant_urls
                        logger.info(f"Found relevant resources for code quality: {relevant_urls}")
        except Exception as se:
            logger.error(f"Error searching for code quality resources: {se}")
            # If search fails, don't worry about it - the LLM can analyze the code
            pass
            
        # Let the LLM handle the detailed analysis
        result["notes"].append("The LLM can perform detailed code analysis based on its knowledge of programming best practices.")
        
    except Exception as e:
        result["error"] = f"Error preparing code analysis resources: {str(e)}"
        logger.error(f"Error in analyze_code: {e}")
    
    return result

@tool
def explain_cultural_concept(concept: str, region: Optional[str] = None) -> str:
    """Retrieves factual information about an Indian cultural concept or tradition to augment the LLM's knowledge.
    Rather than providing a complete response, this tool enriches LLM responses with verified facts and context.
    
    Args:
        concept: The cultural concept, tradition, or practice to explain.
        region: Optional specific Indian region or state for regional context.
    
    Returns:
        Factual context about the cultural concept to supplement the LLM's knowledge.
    """
    logger.info(f"explain_cultural_concept called for concept: {concept}, region: {region}")
    # Use Wikipedia to get information about cultural concepts
    search_query = f"{concept} {region if region else 'India'} culture tradition"
    try:
        # First try searching Wikipedia
        wikipedia.set_lang("en")  # Default to English for most comprehensive results
        search_results = wikipedia.search(search_query, results=3)
        logger.info(f"Wikipedia search results for cultural concept: {search_results}")
        
        facts_and_context = []
        sources = []
        
        # Try Wikipedia
        if search_results:
            try:
                # Get the most relevant page
                page = wikipedia.page(search_results[0], auto_suggest=False)
                content = page.summary
                url = page.url
                
                # Extract key facts from the content
                paragraphs = content.split('\n')
                significant_paragraphs = []
                
                # Keep the first 2 paragraphs which usually contain the most important information
                if paragraphs:
                    significant_paragraphs = paragraphs[:min(2, len(paragraphs))]
                
                # Extract dates and historical context
                dates = re.findall(r'\b\d{3,4}(?:s|\b)', content)
                if dates:
                    facts_and_context.append(f"Historical timeframe: {', '.join(dates[:5])}")
                
                # Extract key people or places
                key_entities = re.findall(r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*', content)
                if key_entities and len(key_entities) > 1:
                    # Filter out common words
                    common_words = ["India", "Indian", "Hindu", "Muslim", "Sikh", "Buddhist", "Jain", "The", "These", "Those", "This", "That"]
                    filtered_entities = [e for e in key_entities if e not in common_words]
                    if filtered_entities:
                        facts_and_context.append(f"Key associated entities: {', '.join(filtered_entities[:5])}")
                
                # Add the summary content
                if significant_paragraphs:
                    facts_and_context.append("\n".join(significant_paragraphs))
                
                sources.append(f"Wikipedia: {url}")
                
                # Add regional context if specified
                if region:
                    # Try to extract region-specific information from the full content
                    regional_info = None
                    if region.lower() in page.content.lower():
                        full_paragraphs = page.content.split('\n\n')
                        for p in full_paragraphs:
                            if region.lower() in p.lower():
                                regional_info = p
                                break
                    
                    if regional_info:
                        facts_and_context.append(f"Regional context for {region}: {regional_info}")
                        logger.info(f"Extracted regional context for {region}")
                
            except (wikipedia.DisambiguationError, wikipedia.PageError) as e:
                # If we hit disambiguation, just note the ambiguity as a fact
                if hasattr(e, 'options'):
                    facts_and_context.append(f"The term '{concept}' has multiple meanings in Indian culture: {', '.join(e.options[:5])}")
                    logger.info(f"Disambiguation noted for concept: {concept}")
        
        # Try web search for additional factual context
        try:
            from smolagents import WebSearchTool
            web_search = WebSearchTool()
            search_results = web_search(search_query)
            logger.info(f"Web search results for cultural concept: {search_results}")
            
            if search_results and len(search_results) > 100:
                # Extract a reasonable portion of the web search results
                excerpt = search_results[:1000]
                sources.append("Web search")
                
                # Extract the most relevant sentences that contain the concept name
                sentences = re.split(r'[.!?]', excerpt)
                relevant_sentences = [s.strip() for s in sentences if concept.lower() in s.lower()][:3]
                
                if relevant_sentences:
                    facts_and_context.append("Additional context from search results: " + " ".join(relevant_sentences))
                    logger.info(f"Relevant sentences from web search: {relevant_sentences}")
        except Exception as we:
            logger.error(f"Error in web search for cultural concept: {we}")
            pass
        
        # Combine all gathered factual information
        if facts_and_context:
            formatted_facts = "\n\n".join(facts_and_context)
            formatted_sources = ", ".join(sources)
            
            return f"## Factual context about {concept}\n\n{formatted_facts}\n\nSources: {formatted_sources}"
        
        # If all searches failed, return a message that lets the LLM use its knowledge
        return f"No definitive factual sources found for '{concept}'. The LLM can rely on its knowledge of Indian cultural concepts."
        
    except Exception as e:
        logger.error(f"Error in explain_cultural_concept: {e}")
        # Fallback that lets the LLM use its own knowledge without errors in the context
        return f"Unable to retrieve external information about '{concept}'. The LLM can proceed with its knowledge of Indian cultural concepts."

@tool
def check_exam_syllabus(exam: str, subject: Optional[str] = None) -> str:
    """Retrieves key sections of the syllabus for Indian competitive exams to augment LLM responses.
    This tool provides factual syllabus information from reliable sources to supplement the LLM's knowledge.
    
    Args:
        exam: The competitive exam code (e.g., "UPSC", "JEE", "NEET").
        subject: Optional specific subject within the exam syllabus.
    
    Returns:
        Key sections or topics from the syllabus for the specified exam.
    """
    logger.info(f"check_exam_syllabus called for exam: {exam}, subject: {subject}")
    try:
        # Define search query based on exam and optional subject
        search_query = f"{exam} {'official' if 'upsc' in exam.lower() else ''} syllabus"
        if subject:
            search_query += f" {subject}"
        
        syllabus_content = []
        source = ""
        
        # First try Wikipedia for general structure
        try:
            wikipedia.set_lang("en")
            wiki_results = wikipedia.search(search_query, results=2)
            logger.info(f"Wikipedia search results for syllabus: {wiki_results}")
            
            if wiki_results:
                try:
                    page = wikipedia.page(wiki_results[0], auto_suggest=False)
                    if page and (exam.lower() in page.title.lower() or 'syllabus' in page.title.lower()):
                        # Extract only the most relevant parts
                        content = page.content
                        source = f"Wikipedia: {page.url}"
                        logger.info(f"Extracted syllabus content from Wikipedia")
                        
                        # Try to find subject-specific content if a subject was provided
                        if subject:
                            # Look for sections that match the subject
                            sections = content.split('\n== ')
                            for section in sections:
                                if subject.lower() in section.lower():
                                    # Extract just the topic headings rather than full content
                                    import re
                                    topics = re.findall(r'\n=== ([^=]+) ===', section)
                                    if topics:
                                        syllabus_content.append(f"Key topics in {subject} for {exam}:")
                                        syllabus_content.append("- " + "\n- ".join(topics))
                                        logger.info(f"Extracted key topics for {subject}: {topics}")
                                    else:
                                        # If no clear topic headings, extract bullet points or numbered lists
                                        points = re.findall(r'\n\* ([^\n]+)|\n\d+\. ([^\n]+)', section)
                                        if points:
                                            syllabus_content.append(f"Key points in {subject} for {exam}:")
                                            flat_points = []
                                            for p in points:
                                                # points may be tuples with empty strings
                                                point = next((item for item in p if item), "")
                                                if point:
                                                    flat_points.append(point)
                                            syllabus_content.append("- " + "\n- ".join(flat_points[:10]))  # Limit to 10 points
                                            logger.info(f"Extracted key points for {subject}: {flat_points[:10]}")
                        # If we can't find subject-specific content or no subject was provided
                        if not syllabus_content:
                            # Extract main sections of the syllabus
                            import re
                            main_sections = re.findall(r'\n== ([^=]+) ==', content)
                            if main_sections:
                                syllabus_content.append(f"Main sections of {exam} syllabus:")
                                syllabus_content.append("- " + "\n- ".join(main_sections))
                            else:
                                # Fall back to the summary
                                summary = page.summary
                                if len(summary) > 500:
                                    # Get just the first paragraph which usually has the most important information
                                    first_para = summary.split('\n')[0]
                                    syllabus_content.append(first_para)
                                else:
                                    syllabus_content.append(summary)
                except Exception as wiki_error:
                    logger.error(f"Error in Wikipedia syllabus extraction: {wiki_error}")
                    pass
        
        # Try web search as a backup for more current information
        try:
            from smolagents import WebSearchTool
            web_search = WebSearchTool()
            search_results = web_search(search_query + " official")
            logger.info(f"Web search results for syllabus: {search_results}")
            
            if search_results and len(search_results) > 150:
                # Extract information about the exam pattern if mentioned
                import re
                
                # Try to find exam pattern information
                pattern_match = re.search(r'(?:exam pattern|test pattern|examination pattern)([^.]+(?:\.[^.]+){0,3})', search_results, re.IGNORECASE)
                if pattern_match:
                    syllabus_content.append(f"Exam pattern: {pattern_match.group(1).strip()}")
                    logger.info(f"Extracted exam pattern information")
                
                # Try to find subject weightage if mentioned
                weightage_match = re.search(r'(?:weightage|marks distribution|subject distribution)([^.]+(?:\.[^.]+){0,2})', search_results, re.IGNORECASE)
                if weightage_match:
                    syllabus_content.append(f"Marks distribution: {weightage_match.group(1).strip()}")
                    logger.info(f"Extracted marks distribution information")
                
                # If web search provided substantial information and we didn't have anything from Wikipedia
                if (pattern_match or weightage_match) and not source:
                    source = "Web search results"
                    logger.info(f"Using web search as the source of syllabus information")
        except Exception as we:
            logger.error(f"Error in web search for syllabus: {we}")
            pass
        
        # Combine all gathered information
        if syllabus_content:
            formatted_content = "\n\n".join(syllabus_content)
            
            return f"## {exam} {'- ' + subject if subject else ''} Syllabus Information\n\n{formatted_content}\n\nSource: {source}"
        
        # If we couldn't find anything specific, return a message that lets the LLM use its knowledge
        return f"Specific syllabus information for {exam} {f'({subject})' if subject else ''} couldn't be retrieved. The LLM can proceed with its knowledge of this examination."
        
    except Exception as e:
        logger.error(f"Error in check_exam_syllabus: {e}")
        return f"Unable to retrieve current syllabus for {exam}. The LLM can provide information based on its training data, but note that examination patterns may have changed."
