"""
Unit tests for the enhanced agent tools in Bharat AI Buddy
"""
import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the tools to test
from agent_tools_improved import (
    solve_math_problem,
    analyze_code,
    search_wikipedia,
    exam_question_generator,
    explain_cultural_concept
)

class TestMathProblemSolver(unittest.TestCase):
    """Tests for the solve_math_problem tool"""
    
    @patch("agent_tools_improved.WebSearchTool")
    def test_simple_arithmetic(self, mock_search_tool):
        """Test that simple arithmetic expressions are calculated correctly"""
        # Mock the search tool to avoid actual web requests during testing
        mock_search_instance = MagicMock()
        mock_search_instance.return_value = "Mock search results"
        mock_search_tool.return_value = mock_search_instance
        
        # Test with a simple arithmetic problem
        result = solve_math_problem("What is 5 + 10?")
        self.assertIn("5+10 = 15", result)
        
    @patch("agent_tools_improved.WebSearchTool")
    def test_search_augmentation(self, mock_search_tool):
        """Test that search results are included for complex problems"""
        # Mock the search tool to return relevant content
        mock_search_instance = MagicMock()
        mock_search_instance.return_value = "To solve quadratic equations, use the quadratic formula x = (-b ± √(b² - 4ac)) / 2a"
        mock_search_tool.return_value = mock_search_instance
        
        # Test with a complex problem that should trigger search
        result = solve_math_problem("How to solve quadratic equation x^2 + 5x + 6 = 0?")
        self.assertIn("quadratic formula", result.lower())

    def test_graceful_failure(self):
        """Test that the tool handles errors gracefully"""
        # Patch eval to raise an exception
        with patch("agent_tools_improved.eval", side_effect=Exception("Test error")):
            # The function should return a message instead of raising an exception
            result = solve_math_problem("What is 5 + 10?")
            self.assertIn("LLM can solve", result)


class TestCodeAnalyzer(unittest.TestCase):
    """Tests for the analyze_code tool"""
    
    def test_basic_code_stats(self):
        """Test that basic code statistics are computed correctly"""
        code = """
def hello_world():
    print("Hello, world!")
    
# Call the function
hello_world()
"""
        result = analyze_code(code, "python")
        self.assertIsInstance(result, dict)
        self.assertIn("basic_stats", result)
        self.assertEqual(result["basic_stats"]["line_count"], 5)
        
    def test_security_pattern_detection(self):
        """Test that critical security patterns are detected"""
        code = """
import os

def execute_command(cmd):
    # This is insecure!
    os.system(cmd)
"""
        result = analyze_code(code, "python")
        self.assertIn("security_concerns", result)
        self.assertTrue(any("os.system" in item for item in result["security_concerns"]))
        
    @patch("agent_tools_improved.WebSearchTool")
    def test_best_practices_search(self, mock_search_tool):
        """Test that best practices are searched for"""
        # Mock the search tool
        mock_search_instance = MagicMock()
        mock_search_instance.return_value = "Python function best practices include descriptive naming and docstrings"
        mock_search_tool.return_value = mock_search_instance
        
        code = "def f(x): return x*2"
        result = analyze_code(code, "python")
        
        # Verify search was called with appropriate terms
        self.assertIn("best_practices", result)
        mock_search_instance.assert_called()


class TestCulturalConceptExplainer(unittest.TestCase):
    """Tests for the explain_cultural_concept tool"""
    
    @patch("agent_tools_improved.search_wikipedia")
    @patch("agent_tools_improved.WebSearchTool")
    def test_cultural_concept_extraction(self, mock_search_tool, mock_wiki_search):
        """Test that cultural concept information is extracted properly"""
        # Mock Wikipedia search
        mock_wiki_search.return_value = "# Diwali\n\nDiwali is the festival of lights celebrated by Hindus, Jains, and Sikhs. The festival usually lasts five days."
        
        # Mock web search
        mock_search_instance = MagicMock()
        mock_search_instance.return_value = "Diwali 2023 will be celebrated on November 12th"
        mock_search_tool.return_value = mock_search_instance
        
        result = explain_cultural_concept("Diwali festival")
        
        # Check that the result combines information from both sources
        self.assertIn("Diwali", result)
        self.assertIn("festival of lights", result)


class TestExamQuestionGenerator(unittest.TestCase):
    """Tests for the exam_question_generator tool"""
    
    @patch("agent_tools_improved.wikipedia")
    def test_exam_format_extraction(self, mock_wikipedia):
        """Test that exam format information is extracted"""
        # Mock Wikipedia search and page content
        mock_wikipedia.search.return_value = ["UPSC Civil Services Examination"]
        mock_page = MagicMock()
        mock_page.content = "== Exam Pattern ==\nThe exam consists of three stages: Prelims, Mains, and Interview."
        mock_page.summary = "The Civil Services Examination is conducted by the UPSC annually."
        mock_wikipedia.page.return_value = mock_page
        
        result = exam_question_generator("UPSC", "General Studies")
        
        # Check that exam pattern information is included
        self.assertIn("Exam", result)
        self.assertIn("Pattern", result)


if __name__ == "__main__":
    unittest.main()
