from model_utils import generate_response
from constants import EXAMS, SUBJECTS

quiz_state = {}

def generate_quiz_question(exam, subject, language):
    prompt = f"Generate a {subject} question for {exam} exam in {language}. Provide 4 options and the correct answer."
    _, answer = generate_response(prompt, "think", language)
    # Expecting answer in format: Q: ...\nA) ...\nB) ...\nC) ...\nD) ...\nAnswer: ...
    return answer

def check_quiz_answer(user_answer, correct_answer):
    return user_answer.strip().lower() == correct_answer.strip().lower()
