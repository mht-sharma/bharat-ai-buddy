from model_utils import generate_response
from constants import EXAMS, SUBJECTS
import logging

quiz_state = {}

def generate_quiz_question(exam, subject):
    logger = logging.getLogger("bharat_buddy")
    logger.info(f"generate_quiz_question called with exam={exam}, subject={subject}")
    prompt = f"Generate a {subject} question for {exam} exam. Provide 4 options and the correct answer."
    _, answer = generate_response(prompt, "think")
    # Expecting answer in format: Q: ...\nA) ...\nB) ...\nC) ...\nD) ...\nAnswer: ...
    return answer

def check_quiz_answer(user_answer, correct_answer):
    logger = logging.getLogger("bharat_buddy")
    logger.info(f"check_quiz_answer called with user_answer={user_answer}, correct_answer={correct_answer}")
    return user_answer.strip().lower() == correct_answer.strip().lower()
