import random
import os
import subprocess
import sys

# Ensure inquirer is installed
subprocess.check_call([sys.executable, "-m", "pip", "install", "inquirer"])

import inquirer

def load_file(file):
    encodings = ['utf-8', 'cp1250', 'latin-1', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    raise UnicodeDecodeError(f"Unable to decode file with any of these encodings: {encodings}")

def split_questions(text):
    questions = []
    current_question = None
    for line in text.split('\n'):
        if line.strip() == '':
            if current_question:
                questions.append(current_question)
                current_question = None
        elif line[0].isdigit():
            if current_question:
                questions.append(current_question)
            current_question = {'question': line, 'answers': [], 'type': 'checkbox'}  # All questions are checkbox type
        elif line.startswith('\t'):
            if current_question:
                current_question['answers'].append(line.strip())
    if current_question:
        questions.append(current_question)
    return questions

def get_answers(text):
    answers = {}
    for line in text.split('\n'):
        if line.strip() and line[0].isdigit():
            question_number, answer = line.split('.', 1)
            # Extract just the letters from the answers (e.g., "a) b)" -> ["a", "b"])
            answer_letters = [a.split(')')[0].strip() for a in answer.split()]
            answers[question_number.strip()] = answer_letters
    return answers


def test_user(questions, correct_answers):
    points = 0
    for q in questions:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Points: {round(points, 2)} / {questions.index(q)}\n")
        question_number = q['question'].split('.')[0]

        # Display question and get user answers
        answer = inquirer.prompt([
            inquirer.Checkbox(
                name='answer',
                message=q['question'],
                choices=q['answers']
            )
        ])
        
        # Extract only the letters (e.g., "a)", "b)") from the user-selected answers
        user_answers = set([a.split(')')[0].strip() for a in answer['answer']])
        correct_set = set(correct_answers.get(question_number, []))

        # Compare user's answers with the correct answers
        if user_answers == correct_set:
            print("Correct!\n")
            points += 1
        else:
            correct_formatted = ', '.join(correct_answers.get(question_number, []))
            print(f"Wrong, the correct answers are {correct_formatted}\n")

        input("Press Enter ⏎ to continue")



def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    # Course Selection
    course_questions = [
        inquirer.List(
            'course',
            message="Select course",
            choices=['PIB', 'IAU'],
        )
    ]
    course_answer = inquirer.prompt(course_questions)
    course = course_answer['course']

    if course == 'PIB':
        file = 'PIB_Qs.md'
        file2 = 'PIB_answers.md'
    elif course == 'IAU':
        file = 'terminal_friendly.md'
        file2 = 'IAU Odpovede.md'

    text = load_file(file)
    answers_text = load_file(file2)

    questions = split_questions(text)
    correct_answers = get_answers(answers_text)

    # Mode Selection
    mode_questions = [
        inquirer.List(
            'mode',
            message="Select mode",
            choices=['Sequential', 'Random', '30 Questions Test', 'Starting with...'],
        )
    ]
    mode_answer = inquirer.prompt(mode_questions)
    mode = mode_answer['mode']

    if mode == 'Random':
        random.shuffle(questions)
    elif mode == '30 Questions Test':
        questions = random.sample(questions, 30)
    elif mode == 'Starting with...':
        start_question = inquirer.prompt([
            inquirer.Text('start', message="Start from question number")
        ])
        start = int(start_question['start'])
        questions = questions[start - 1:start + 35]

    test_user(questions, correct_answers)

if __name__ == "__main__":
    main()
