# ui.py
"""
UI construction and Gradio wiring for Bharat AI Buddy
"""
import gradio as gr
from constants import LANGUAGES, EXAMPLES, TRENDING, EXAMS, SUBJECTS, REGIONS, REGIONAL_TOPICS
from app_logic import (
    app_fn, example_click, trending_click, update_subjects, 
    start_quiz_fn, submit_answer_fn, get_syllabus_info,
    get_study_tips, exam_qa, generate_regional_query
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
                <b>नमस्ते! Welcome! வணக்கம்! স্বাগதம! स्वागत है!</b>
            </div>
            <div style='font-size:0.9em; margin-top:0.5em; padding: 5px; background-color:#f8f8f8; border-radius:8px;'>
                <img src='https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.png' alt='Powered by' style='height:24px; vertical-align:middle; margin-right:5px;'>
                <span style='vertical-align:middle;'>Powered by <b style='color:#6366f1;'>Sarvam-M</b> — <i>India's own multilingual AI model</i></span>
            </div>
        </div>
        """)
        with gr.Row():
            language = gr.Dropdown([l[0] for l in LANGUAGES], value="English", label="Language", elem_id="lang-select")
            mode = gr.Radio(["think", "non-think"], value="think", label="Mode", elem_id="mode-select")
            use_agents = gr.Checkbox(value=True, label="Use AI Agents", info="Enables specialized AI agents for advanced capabilities")
        with gr.Tabs() as tabs:
            for tab_name, icon in zip(EXAMPLES.keys(), ["🧮", "💻", "🎉", "🌏"]):
                with gr.Tab(f"{icon} {tab_name}"):
                    with gr.Row():
                        prompt = gr.Textbox(label=f"Ask your {tab_name.lower()} question (in any Indian language)", lines=2, elem_id=f"prompt-{tab_name}")
                    
                    # Add file upload capabilities for relevant tabs
                    if tab_name == "Code":
                        with gr.Row():
                            file_upload = gr.File(label="Upload code file for analysis", file_types=[".py", ".js", ".html", ".css", ".cpp", ".java", ".go", ".ts"])
                    elif tab_name == "Culture":
                        with gr.Row():
                            image_upload = gr.Image(label="Upload image for cultural analysis", type="filepath")
                    elif tab_name == "Regional":
                        with gr.Row():
                            with gr.Column(scale=1):
                                region = gr.Dropdown(
                                    list(REGIONS.keys()), 
                                    value="North India", 
                                    label="Select Region", 
                                    elem_id=f"region-select"
                                )
                            with gr.Column(scale=1):
                                state = gr.Dropdown(
                                    REGIONS["North India"], 
                                    value=REGIONS["North India"][0], 
                                    label="Select State", 
                                    elem_id=f"state-select"
                                )
                            with gr.Column(scale=1):
                                topic = gr.Dropdown(
                                    list(REGIONAL_TOPICS.keys()),
                                    value="Cuisines", 
                                    label="Select Topic", 
                                    elem_id=f"topic-select"
                                )
                        with gr.Row():
                            topic_description = gr.Textbox(
                                value=REGIONAL_TOPICS["Cuisines"],
                                label="Topic Description",
                                interactive=False
                            )
                        with gr.Row():
                            regional_prompt = gr.Textbox(
                                placeholder="Optional: Add specific questions about this regional topic...",
                                label="Optional Custom Query", 
                                lines=2
                            )
                        with gr.Row():
                            generate_btn = gr.Button("Explore Regional Knowledge", variant="primary")
                        with gr.Row():
                            gr.HTML("""
                            <div style='text-align:center; padding: 5px; background-color:#f0f8ff; border-radius:5px; margin-bottom:10px;'>
                                <span style='color:#444;'>👑 <b>Sarvam's Regional Expertise</b> - Experience deep understanding of India's diverse cultures</span>
                            </div>
                            """)
                    
                    with gr.Row():
                        example_btns = [gr.Button(example, elem_id=f"ex-{i}-{tab_name}") for i, example in enumerate(EXAMPLES[tab_name])]
                    with gr.Row():
                        trending_btns = [gr.Button(tr, elem_id=f"tr-{i}-{tab_name}") for i, tr in enumerate(TRENDING)]
                    output = gr.Textbox(label="Response", lines=8, elem_id=f"output-{tab_name}")
                    submit = gr.Button("Submit", elem_id=f"submit-{tab_name}", scale=2)
                    submit.click(app_fn, inputs=[gr.State(tab_name), prompt, mode, language, use_agents], outputs=output)
                    for btn, example in zip(example_btns, EXAMPLES[tab_name]):
                        btn.click(example_click, inputs=[gr.State(tab_name), gr.State(example), mode, language, use_agents], outputs=output)
                    for btn, tr in zip(trending_btns, TRENDING):
                        btn.click(trending_click, inputs=[gr.State(tab_name), gr.State(tr), mode, language, use_agents], outputs=output)
                    gr.Markdown("<hr style='border:1px solid #ff9933;'>")
                    gr.HTML("""
                    <div style='text-align:center; color:#388e3c; margin-bottom:0.5em;'>
                        <b>Share your answer:</b>
                        <a href='#' onclick='navigator.share ? navigator.share({text: document.getElementById("output-{tab_name}").value}) : alert("Copy and share manually!")' style='margin:0 8px;'><img src='https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg' width='28' style='vertical-align:middle;'></a>
                        <a href='https://www.instagram.com/' target='_blank' style='margin:0 8px;'><img src='https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png' width='28' style='vertical-align:middle;'></a>
                        <a href='https://x.com/' target='_blank' style='margin:0 8px;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/53/X_logo_2023.svg' width='28' style='vertical-align:middle;'></a>
                    </div>
                    """)
            with gr.Tab("🏆 Exam Prep Buddy"):
                with gr.Tabs() as exam_tabs:
                    with gr.Tab("Quiz Mode"):
                        with gr.Row():
                            exam = gr.Dropdown(EXAMS, value="UPSC", label="Exam", elem_id="exam-select")
                            subject = gr.Dropdown(SUBJECTS["UPSC"], value="History", label="Subject", elem_id="subject-select")
                            language_quiz = gr.Dropdown([l[0] for l in LANGUAGES], value="English", label="Language", elem_id="quiz-lang-select")
                        with gr.Row():
                            start_quiz = gr.Button("Start Quiz", elem_id="start-quiz-btn", scale=2)
                        quiz_question = gr.Textbox(label="Question", lines=4, interactive=False, elem_id="quiz-question")
                        user_answer = gr.Textbox(label="Your Answer (A/B/C/D)", lines=1, elem_id="quiz-user-answer")
                        submit_answer = gr.Button("Submit Answer", elem_id="quiz-submit-btn")
                        quiz_feedback = gr.Textbox(label="Feedback", lines=3, interactive=False, elem_id="quiz-feedback")
                    
                    with gr.Tab("Syllabus Guide"):
                        with gr.Row():
                            exam_syllabus = gr.Dropdown(EXAMS, value="UPSC", label="Exam", elem_id="syllabus-exam-select")
                            subject_syllabus = gr.Dropdown(SUBJECTS["UPSC"], value="History", label="Subject", elem_id="syllabus-subject-select")
                        with gr.Row():
                            get_syllabus_btn = gr.Button("Get Detailed Syllabus", elem_id="get-syllabus-btn")
                            get_tips_btn = gr.Button("Get Study Tips", elem_id="get-tips-btn")
                        syllabus_output = gr.Textbox(label="Syllabus Information", lines=8, elem_id="syllabus-output")
                        
                    with gr.Tab("Exam Q&A"):
                        with gr.Row():
                            exam_qa = gr.Dropdown(EXAMS, value="UPSC", label="Exam", elem_id="qa-exam-select")
                            subject_qa = gr.Dropdown(SUBJECTS["UPSC"], value="History", label="Subject", elem_id="qa-subject-select")
                        with gr.Row():
                            qa_prompt = gr.Textbox(label="Ask about exam preparation", lines=2, elem_id="qa-prompt")
                            qa_language = gr.Dropdown([l[0] for l in LANGUAGES], value="English", label="Language", elem_id="qa-lang-select")
                        qa_submit = gr.Button("Get Answer", elem_id="qa-submit-btn")
                        qa_output = gr.Textbox(label="Answer", lines=8, elem_id="qa-output")
                gr.HTML("""
                <div style='text-align:center; color:#388e3c; margin-bottom:0.5em;'>
                    <b>Share your quiz result:</b>
                    <a href='#' onclick='navigator.share ? navigator.share({text: document.getElementById("quiz-feedback").value}) : alert("Copy and share manually!")' style='margin:0 8px;'><img src='https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg' width='28' style='vertical-align:middle;'></a>
                    <a href='https://www.instagram.com/' target='_blank' style='margin:0 8px;'><img src='https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png' width='28' style='vertical-align:middle;'></a>
                    <a href='https://x.com/' target='_blank' style='margin:0 8px;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/53/X_logo_2023.svg' width='28' style='vertical-align:middle;'></a>
                </div>
                """)
                # Connect the exam dropdowns to update subjects
                exam.change(update_subjects, inputs=exam, outputs=subject)
                exam_syllabus.change(update_subjects, inputs=exam_syllabus, outputs=subject_syllabus)
                exam_qa.change(update_subjects, inputs=exam_qa, outputs=subject_qa)
                
                # Connect the syllabus buttons to their functions
                get_syllabus_btn.click(get_syllabus_info, inputs=[exam_syllabus, subject_syllabus], outputs=syllabus_output)
                get_tips_btn.click(get_study_tips, inputs=[exam_syllabus, subject_syllabus], outputs=syllabus_output)
                
                # Connect the Q&A functionality
                qa_submit.click(exam_qa, inputs=[exam_qa, subject_qa, qa_prompt, qa_language], outputs=qa_output)
                start_quiz.click(start_quiz_fn, inputs=[exam, subject, language_quiz], outputs=[quiz_question, quiz_feedback])
                submit_answer.click(submit_answer_fn, inputs=user_answer, outputs=quiz_feedback)
                
                # Regional tab functionality
                region.change(lambda r: gr.Dropdown.update(choices=REGIONS[r], value=REGIONS[r][0]), inputs=region, outputs=state)
                topic.change(lambda t: REGIONAL_TOPICS[t], inputs=topic, outputs=topic_description)
                
                # Connect regional exploration button
                if 'Regional' in EXAMPLES:
                    for tab_index, tab_name in enumerate(EXAMPLES.keys()):
                        if tab_name == "Regional":
                            with tabs[tab_index]:
                                generate_btn.click(
                                    generate_regional_query, 
                                    inputs=[region, state, topic, language, regional_prompt], 
                                    outputs=output
                                )
        gr.HTML("""
        <div style='text-align:center; margin-top:1.5em; color:#1a237e; font-size:1.1em;'>
            <b>Made with ❤️ in India | भारत में निर्मित</b>
        </div>
        """)
    return demo
