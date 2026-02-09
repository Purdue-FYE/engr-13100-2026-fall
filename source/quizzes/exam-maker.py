import random
from pathlib import Path

QUESTION_BANK = Path("Excel Question Banks")
OUTPUT_DIR = Path("quizzes")
OUTPUT_DIR.mkdir(exist_ok=True)

# exam design
EXAM_STRUCTURE = {
    "loops": 2,
    "arrays": 1,
    "matlab_basics": 2
}

NUM_VERSIONS = 3
SEED = 42  # remove or change for different exams

random.seed(SEED)

def load_questions(folder):
    return list(folder.glob("*.md"))

for version in range(NUM_VERSIONS):
    exam_questions = []

    for topic, count in EXAM_STRUCTURE.items():
        questions = load_questions(QUESTION_BANK / topic)
        chosen = random.sample(questions, count)
        exam_questions.extend(chosen)

    random.shuffle(exam_questions)

    exam_text = "# Exam Version {}\n\n".format(chr(65 + version))

    for i, q in enumerate(exam_questions, start=1):
        exam_text += f"## Question {i}\n\n"
        exam_text += q.read_text() + "\n\n"

    output_file = OUTPUT_DIR / f"exam_{chr(65 + version)}.md"
    output_file.write_text(exam_text)

    print(f"Generated {output_file}")
