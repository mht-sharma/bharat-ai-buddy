# 🇮🇳 Bharat AI Buddy

A high-impact, multilingual, and viral-ready Hugging Face Space powered by the Sarvam-M model and enhanced with smolagents toolkit.

## ✨ Features

**Core Capabilities:**
- Direct queries in major Indian languages: Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati (with automatic language detection)
- Math, code, and cultural Q&A with responses in your preferred Indian language
- Regional knowledge tab showcasing Sarvam's deep understanding of India's diverse cultures
- Exam Prep Buddy: UPSC, JEE, NEET, SSC, Bank PO, GATE quizzes with instant feedback
- Step-by-step ("think") and concise ("non-think") reasoning modes
- Share answers and quiz results to WhatsApp, Instagram, and X
- Modern, India-inspired UI

**Advanced Agent-powered Features:**
- **Domain-Specific AI Agents**: Specialized agents for math, coding, exam prep, and cultural topics
- **Code Generation & Execution**: Live code analysis and generation with the CodeAgent
- **Web Intelligence**: Real-time web search and page analysis for current affairs and research
- **Math Problem Solving**: Step-by-step math solutions with intuitive explanations
- **Document & Image Analysis**: Extract text from documents and analyze images (experimental)
- **Cultural Context**: Deep understanding of Indian cultural contexts with reliable sources

## 🧠 Powered by smolagents

This app leverages [smolagents](https://github.com/huggingface/smolagents) from Hugging Face to provide intelligent, tool-using capabilities:
- Multi-step reasoning with specialized agents for different knowledge domains
- Secure code execution capabilities for programming tasks
- Web search and website analysis for real-time information

## Quickstart

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the app:**
   ```bash
   python app.py
   ```
3. **(Optional) Run with Docker:**
   ```bash
   docker build -t bharat-ai-buddy .
   docker run -p 7860:7860 bharat-ai-buddy
   ```

## Requirements

- Python 3.9+
- See `requirements.txt` for all dependencies, including:
  - gradio, transformers, torch
  - smolagents[toolkit], markdownify, wikipedia, duckduckgo-search

## Usage Notes
- For trending/culture/news queries, the app uses a multi-agent system to fetch and summarize the latest info from the web.
- For math, code, and exam prep, it uses the Sarvam-M model for step-by-step or concise answers.
- You can easily extend with more tools or agents for even richer answers.

## Project Structure

- `app.py` — Gradio UI and app entry point
- `constants.py` — Static data (languages, examples, exams, etc.)
- `model_utils.py` — Model loading and response generation
- `quiz.py` — Quiz logic and state

## Model
Uses [sarvamai/sarvam-m](https://huggingface.co/sarvamai/sarvam-m) for all reasoning and generation.

## Customization
- Add new tabs or features by extending `app.py` and modular files.
- To add more exams, update `constants.py`.

## Credits
- Built with ❤️ in India using [Gradio](https://gradio.app/) and [Transformers](https://huggingface.co/docs/transformers/index).
- Model by [SarvamAI](https://huggingface.co/sarvamai/sarvam-m).
