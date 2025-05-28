# tests/test_app.py
"""
Automated tests for Bharat AI Buddy backend and UI
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app_logic import app_fn, exam_qa, get_syllabus_info, get_study_tips, start_quiz_fn, submit_answer_fn
from constants import EXAMPLES
import gradio as gr
import ui
import logging

logger = logging.getLogger("bharat_buddy")
logger.info("test_app.py loaded.")

# --- Backend Unit Tests ---
def test_app_fn_basic():
    logger.info("Running test_app_fn_basic")
    for tab in EXAMPLES.keys():
        resp = app_fn(tab, "Test prompt", "think", True)
        assert isinstance(resp, str) and len(resp) > 0

def test_app_fn_empty():
    logger.info("Running test_app_fn_empty")
    resp = app_fn("Math", "", "think", True)
    assert isinstance(resp, str)

def test_exam_qa():
    logger.info("Running test_exam_qa")
    out = exam_qa("UPSC", "History", "How to prepare?", None)
    assert isinstance(out, str) and len(out) > 0

def test_get_syllabus_info():
    logger.info("Running test_get_syllabus_info")
    out = get_syllabus_info("UPSC", "History")
    assert isinstance(out, str)

def test_get_study_tips():
    logger.info("Running test_get_study_tips")
    out = get_study_tips("UPSC", "History")
    assert isinstance(out, str)

def test_start_quiz_fn():
    logger.info("Running test_start_quiz_fn")
    quiz = start_quiz_fn("UPSC", "History")
    assert quiz and "question" in quiz

def test_submit_answer_fn():
    logger.info("Running test_submit_answer_fn")
    quiz = start_quiz_fn("UPSC", "History")
    q = quiz["question"]
    out = submit_answer_fn("UPSC", "History", q, "A")
    assert isinstance(out, str)

# --- Gradio UI Smoke Test ---
def test_gradio_ui_launch():
    logger.info("Running test_gradio_ui_launch")
    demo = ui.build_ui()
    assert isinstance(demo, gr.Blocks)
    # Optionally launch in test mode: demo.launch(prevent_thread_lock=True)

# --- Example Dropdown Logic ---
def test_example_dropdown_populates_prompt():
    logger.info("Running test_example_dropdown_populates_prompt")
    # Simulate the lambda used in example_dropdown.change
    for tab, examples in EXAMPLES.items():
        for ex in examples:
            val = (lambda ex: gr.update(value=ex if ex else "", interactive=True))(ex)
            assert val["value"] == ex
        val_none = (lambda ex: gr.update(value=ex if ex else "", interactive=True))(None)
        assert val_none["value"] == ""
