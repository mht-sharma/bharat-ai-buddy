from smolagents import TransformersModel

engine = TransformersModel(
    model_id="sarvamai/sarvam-m",
    device="cuda",
    max_new_tokens=5000,
    do_sample=True,
)


def generate_response(prompt, mode):
    # Compose chat template for Sarvam-M
    messages = [{"role": "user", "content": prompt}]
    # smolagents expects messages as a list of dicts with 'role' and 'content' as string, not nested lists
    output = engine(messages)
    # output can be a list of dicts or a string
    if isinstance(output, list) and len(output) > 0 and isinstance(output[0], dict) and "content" in output[0]:
        output_text = output[0]["content"]
    else:
        output_text = str(output)
    # Parse Sarvam-M output for reasoning and answer
    if "</think>" in output_text:
        reasoning_content = output_text.split("</think>")[0].rstrip("\n")
        content = output_text.split("</think>")[-1].lstrip("\n").rstrip("</s>")
    else:
        reasoning_content = ""
        content = output_text.rstrip("</s>")
    return reasoning_content, content
