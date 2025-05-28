from smolagents import VLLMModel

sarvam_vllm = VLLMModel(
    model_id="sarvamai/sarvam-m",
    model_kwargs={"max_model_len": 8192},
)



def generate_response(prompt, mode, language):
    # Compose chat template for Sarvam-M
    messages = [{"role": "user", "content": prompt}]
    # Set thinking mode via extra_body
    extra_body = {"chat_template_kwargs": {"enable_thinking": mode == "think"}}
    output = sarvam_vllm(messages, extra_body=extra_body)
    output_text = output[0]["content"] if isinstance(output, list) and "content" in output[0] else str(output)
    # Parse Sarvam-M output for reasoning and answer
    if "</think>" in output_text:
        reasoning_content = output_text.split("</think>")[0].rstrip("\n")
        content = output_text.split("</think>")[-1].lstrip("\n").rstrip("</s>")
    else:
        reasoning_content = ""
        content = output_text.rstrip("</s>")
    return reasoning_content, content
