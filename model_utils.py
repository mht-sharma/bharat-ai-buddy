from smolagents import TransformersModel
import logging

engine = TransformersModel(
    model_id="meta-llama/Llama-3.2-1B-Instruct",
    device="cuda",
    max_new_tokens=5000,
    do_sample=True,
)


def generate_response(prompt, mode):
    logger = logging.getLogger("bharat_buddy")
    logger.debug(f"generate_response called with prompt: {prompt[:200]}... mode: {mode}")
    try:
        # Compose chat template for Sarvam-M
        messages = [{"role": "user", "content": [{"text": prompt}]}]
        logger.debug(f"Sending messages to engine: {messages}")
        # smolagents expects messages as a list of dicts with 'role' and 'content' as a list of dicts with 'text'
        output = engine(messages)
        logger.debug(f"Raw output from engine: {output}")
        # output can be a list of dicts or a string
        if isinstance(output, list) and len(output) > 0 and isinstance(output[0], dict) and "content" in output[0]:
            output_text = output[0]["content"]
        else:
            output_text = str(output)
        logger.debug(f"Output text: {output_text[:500]}")
        # Parse Sarvam-M output for reasoning and answer
        if "</think>" in output_text:
            reasoning_content = output_text.split("</think>")[0].rstrip("\n")
            content = output_text.split("</think>")[-1].lstrip("\n").rstrip("</s>")
        else:
            reasoning_content = ""
            content = output_text.rstrip("</s>")
        logger.debug(f"Reasoning: {reasoning_content[:300]}")
        logger.debug(f"Content: {content[:300]}")
        return reasoning_content, content
    except Exception as e:
        logger.error(f"Error in generate_response: {e}", exc_info=True)
        return "", f"[ERROR] {e}"
