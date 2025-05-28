# ui.py
"""
UI construction and Gradio wiring for Bharat AI Buddy
"""
import gradio as gr
from constants import EXAMPLES
from app_logic import (
    app_fn, example_click, update_subjects, 
    start_quiz_fn, submit_answer_fn, get_syllabus_info,
    get_study_tips, exam_qa as exam_qa_fn
)
from config import config

def build_ui():
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="orange", secondary_hue="green")) as demo:
        gr.HTML("""
        <div style='text-align:center; padding: 1em 0; background: linear-gradient(90deg, #ff9933 0%, #ffffff 50%, #138808 100%); border-radius: 12px;'>
            <img src='https://em-content.zobj.net/source/microsoft-teams/363/robot_1f916.png' alt='Bharat Buddy' style='width:60px; vertical-align:middle; margin-right:10px;'>
            <span style='font-size:2.5em; color:#1a237e; font-weight:bold;'>🇮🇳 Bharat AI Buddy</span>
            <div style='font-size:1.1em; color:#333; margin-top:0.5em;'>
                <b>Math, Code, Culture, and Exam Prep in your language.<br>Step-by-step or concise—your choice!</b>
            </div>
            <div style='font-size:1em; color:#388e3c; margin-top:0.5em;'>
                <b>नमस्ते! Welcome! வணக்கம்! স্বাগতাম! स्वागत है!</b>
            </div>
            <div style='font-size:0.9em; margin-top:0.5em; padding: 5px; background-color:#f8f8f8; border-radius:8px;'>
                <img src='https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.png' alt='Powered by' style='height:24px; vertical-align:middle; margin-right:5px;'>
                <span style='vertical-align:middle; color:#6366f1;'>Powered by <b>Sarvam-M</b> — <i>India's own multilingual AI model</i></span>
            </div>
        </div>
        """)
        with gr.Row():
            mode = gr.Radio(["think", "non-think"], value="think", label="Mode", elem_id="mode-select")
            use_agents = gr.Checkbox(value=True, label="Use AI Agents", info="Enables specialized AI agents for advanced capabilities")
        with gr.Tabs() as tabs:
            for tab_name, icon in zip(EXAMPLES.keys(), ["🧮", "💻", "🎉", "🌏"]):
                with gr.Tab(f"{icon} {tab_name}"):
                    with gr.Row():
                        with gr.Column(scale=8):
                            prompt = gr.Textbox(label=f"Ask your {tab_name.lower()} question (in any Indian language)", lines=2, elem_id=f"prompt-{tab_name}", interactive=True)
                        with gr.Column(scale=4):
                            example_dropdown = gr.Dropdown(
                                choices=[None] + EXAMPLES[tab_name],
                                value=None,
                                label="Choose Example",
                                elem_id=f"example-dropdown-{tab_name}"
                            )
                            example_dropdown.change(lambda ex: gr.update(value=ex if ex else "", interactive=True), inputs=example_dropdown, outputs=prompt)
                    output = gr.Textbox(label="Response", lines=8, elem_id=f"output-{tab_name}")
                    submit = gr.Button("Submit", elem_id=f"submit-{tab_name}", scale=2)
                    # Use prompt as a direct input, not gr.State(tab_name)
                    submit.click(app_fn, inputs=[tab_name, prompt, mode, use_agents], outputs=output)
                with gr.Tab("🏆 Exam Prep Buddy"):
                    with gr.Tabs() as exam_tabs:
                        with gr.Tab("Quiz Mode"):
                            with gr.Row():
                                exam = gr.Textbox(label="Exam", value="UPSC", elem_id="exam-select")
                                subject = gr.Textbox(label="Subject", value="History", elem_id="subject-select")
                            with gr.Row():
                                start_quiz = gr.Button("Start Quiz", elem_id="start-quiz-btn", scale=2)
                            quiz_question = gr.Textbox(label="Question", lines=4, interactive=False, elem_id="quiz-question")
                            user_answer = gr.Textbox(label="Your Answer (A/B/C/D)", lines=1, elem_id="quiz-user-answer")
                            submit_answer = gr.Button("Submit Answer", elem_id="quiz-submit-btn")
                            quiz_feedback = gr.Textbox(label="Feedback", lines=3, interactive=False, elem_id="quiz-feedback")
                        with gr.Tab("Syllabus Guide"):
                            with gr.Row():
                                exam_syllabus = gr.Textbox(label="Exam", value="UPSC", elem_id="syllabus-exam-select")
                                subject_syllabus = gr.Textbox(label="Subject", value="History", elem_id="syllabus-subject-select")
                            with gr.Row():
                                get_syllabus_btn = gr.Button("Get Detailed Syllabus", elem_id="get-syllabus-btn")
                                get_tips_btn = gr.Button("Get Study Tips", elem_id="get-tips-btn")
                            syllabus_output = gr.Textbox(label="Syllabus Information", lines=8, elem_id="syllabus-output")
                        with gr.Tab("Exam Q&A"):
                            with gr.Row():
                                exam_qa = gr.Textbox(label="Exam", value="UPSC", elem_id="qa-exam-select")
                                subject_qa = gr.Textbox(label="Subject", value="History", elem_id="qa-subject-select")
                            with gr.Row():
                                qa_prompt = gr.Textbox(label="Ask about exam preparation", lines=2, elem_id="qa-prompt")
                            qa_submit = gr.Button("Get Answer", elem_id="qa-submit-btn")
                            qa_output = gr.Textbox(label="Answer", lines=8, elem_id="qa-output")
                            qa_submit.click(lambda exam, subject, prompt: exam_qa_fn(exam, subject, prompt, None), inputs=[exam_qa, subject_qa, qa_prompt], outputs=qa_output)
                    get_syllabus_btn.click(get_syllabus_info, inputs=[exam_syllabus, subject_syllabus], outputs=syllabus_output)
                    get_tips_btn.click(get_study_tips, inputs=[exam_syllabus, subject_syllabus], outputs=syllabus_output)
                    
            gr.HTML("""
            <div style='text-align:center; margin-top:1.5em; color:#1a237e; font-size:1.1em;'>
                <b>Made with ❤️ in India | भारत में निर्मित</b>
            </div>
            """)
        return demo
