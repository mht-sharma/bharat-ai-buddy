"""
Document and image processing tools for Bharat AI Buddy
"""
from smolagents import tool
from typing import Optional, Dict, Any, List, Union
import os
import base64
from io import BytesIO

# Only import these if they're needed, to avoid installation issues
def _import_image_libs():
    global Image, np, pytesseract, pdf2image
    from PIL import Image
    import numpy as np
    import pytesseract
    import pdf2image

@tool
def analyze_image(image_data: str) -> Dict[str, Any]:
    """Analyzes an image and extracts text and basic visual information.
    
    Args:
        image_data: Base64 encoded image data.
        
    Returns:
        A dictionary with extracted text and basic image information.
    """
    try:
        _import_image_libs()
        
        # Convert base64 to image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # Extract basic image info
        width, height = image.size
        format_type = image.format
        mode = image.mode
        
        # Extract text if any
        try:
            text = pytesseract.image_to_string(image)
        except:
            text = "No text could be extracted from the image."
            
        return {
            "size": f"{width}x{height}",
            "format": format_type,
            "mode": mode,
            "extracted_text": text if text.strip() else "No text detected in image.",
            "analysis": "Basic image analysis complete."
        }
    except Exception as e:
        return {"error": f"Failed to analyze image: {str(e)}"}

@tool
def extract_text_from_pdf(pdf_path: str, pages: Optional[List[int]] = None) -> Dict[str, Any]:
    """Extracts text from a PDF document.
    
    Args:
        pdf_path: Path to the PDF file.
        pages: Optional list of page numbers to extract (0-indexed).
        
    Returns:
        A dictionary with extracted text by page.
    """
    try:
        _import_image_libs()
        
        # Check if file exists
        if not os.path.exists(pdf_path):
            return {"error": f"File not found: {pdf_path}"}
            
        # Convert PDF to images
        pdf_pages = pdf2image.convert_from_path(pdf_path)
        
        # Filter pages if specified
        if pages is not None:
            pdf_pages = [pdf_pages[i] for i in pages if 0 <= i < len(pdf_pages)]
        
        results = {}
        # Extract text from each page
        for i, page in enumerate(pdf_pages):
            page_num = pages[i] if pages is not None else i
            text = pytesseract.image_to_string(page)
            results[f"page_{page_num}"] = text
            
        return {
            "total_pages": len(pdf_pages),
            "extracted_pages": len(results),
            "text": results
        }
    except Exception as e:
        return {"error": f"Failed to extract text from PDF: {str(e)}"}

@tool
def summarize_document(text: str, max_length: int = 500) -> str:
    """Extracts key information from a long document to augment LLM responses.
    
    Args:
        text: The text content to analyze and extract key information from.
        max_length: Maximum length of the extracted information in characters.
        
    Returns:
        Key facts, dates, statistics and important points from the document that an LLM can use.
    """
    import re
    from collections import Counter
    
    extracted_info = []
    
    # Extract facts, dates, and statistics
    
    # Look for dates (various formats)
    dates = re.findall(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b|\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{2,4}\b', text)
    if dates:
        extracted_info.append("Dates mentioned: " + ", ".join(dates[:5]))
    
    # Look for numbers and statistics
    stats = re.findall(r'\b\d+(?:\.\d+)?%|\b\d+(?:,\d{3})+\b|\₹\d+(?:,\d{3})*(?:\.\d+)?', text)
    if stats:
        extracted_info.append("Key statistics: " + ", ".join(stats[:5]))
    
    # Extract named entities (simplified approach)
    # This is simplified, ideally you'd use a proper NER model
    words = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*\b', text)
    word_counts = Counter(words)
    important_entities = [word for word, count in word_counts.most_common(5) if len(word) > 1 and count > 1]
    if important_entities:
        extracted_info.append("Key entities: " + ", ".join(important_entities))
    
    # Extract sentences that seem important (contain keywords)
    important_keywords = ["important", "significant", "crucial", "essential", "key", "main", "primary", "critical", "fundamental"]
    sentences = re.split(r'[.!?]', text)
    important_sentences = [s.strip() for s in sentences if any(keyword in s.lower() for keyword in important_keywords)]
    if important_sentences:
        extracted_info.append("Key points: " + " ".join(important_sentences[:2]))
    
    # Combine all extracted information
    result = "\n\n".join(extracted_info)
    
    # Truncate if necessary
    if len(result) <= max_length:
        return result
    
    return result[:max_length] + "... (additional information available)"
