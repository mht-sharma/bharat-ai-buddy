"""
UI components for collecting multilingual response feedback in Bharat AI Buddy
"""
import gradio as gr
from feedback_handler import save_feedback

def create_feedback_ui():
    """
    Create UI components for collecting user feedback
    
    Returns:
        Tuple of (feedback_container, submit_feedback_fn)
    """
    with gr.Row(visible=False) as feedback_container:
        with gr.Column():
            gr.Markdown("#### Help us improve multilingual responses")
            with gr.Row():
                rating = gr.Slider(
                    minimum=1, 
                    maximum=5, 
                    value=4, 
                    step=1, 
                    label="How would you rate this response?",
                    interactive=True
                )
            with gr.Row():
                feedback_comment = gr.Textbox(
                    label="Additional comments (optional)", 
                    lines=2,
                    placeholder="Please share any specific feedback about the language, accuracy, or helpfulness..."
                )
            with gr.Row():
                submit_btn = gr.Button("Submit Feedback", variant="primary")
                skip_btn = gr.Button("Skip")
    
    # Hidden fields to store context
    prompt_store = gr.State("")
    response_store = gr.State("")
    
    def submit_feedback(prompt, response, rating_val, comment):
        """Submit feedback and hide the feedback UI"""
        save_feedback(prompt, response, rating_val, comment)
        return gr.update(visible=False), "", ""
    
    def skip_feedback():
        """Hide the feedback UI without submitting"""
        return gr.update(visible=False), "", ""
    
    # Connect the buttons
    submit_btn.click(
        fn=submit_feedback,
        inputs=[prompt_store, response_store, rating, feedback_comment],
        outputs=[feedback_container, feedback_comment, response_store]
    )
    
    skip_btn.click(
        fn=skip_feedback,
        inputs=[],
        outputs=[feedback_container, feedback_comment, response_store]
    )
    
    def show_feedback_ui(prompt, response):
        """
        Show the feedback UI for multilingual responses
        
        Args:
            prompt: User's original query
            response: AI's response
            
        Returns:
            Updates for the UI components
        """
        # Always show feedback UI (language detection removed)
        return gr.update(visible=True), prompt, response, ""
    
    return feedback_container, prompt_store, response_store, show_feedback_ui
