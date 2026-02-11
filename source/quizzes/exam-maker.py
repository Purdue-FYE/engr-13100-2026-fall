import random
import shutil
from pathlib import Path
from datetime import datetime

# This function creates exam versions by randomly selecting questions from
# a structured question bank stored in folders. Each exam version is saved
# as a Markdown file, along with any associated image files in a new directory within /quizzes.

# Inputs: None
# Outputs: Multiple exam Markdown files and associated images in an output directory.
# Author: Andrew Gray
# With assistance from: ChatGPT, Copilot


# CONFIGURATION

#QUESTION_BANK = Path("Excel Question Banks")  # Root folder for question banks
#OUTPUT_DIR = Path("quizzes")                  # Folder for generated quizzes
#OUTPUT_DIR.mkdir(exist_ok=True)               # Ensure output folder exists

BASE_DIR = Path(__file__).resolve().parent
QUESTION_BANK = BASE_DIR / "Excel Question Banks"
#OUTPUT_DIR = BASE_DIR

OUTPUT_DIR = BASE_DIR / f"exam_output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
OUTPUT_DIR.mkdir()

# Define the structure of the exam
# Keys = folder paths inside QUESTION_BANK
# Values = number of questions to pull from that folder
EXAM_STRUCTURE = {
    "Descriptive Analysis & Data Quality/Comparison of Groups": 1,
    "Descriptive Analysis & Data Quality/Conditional Summaries": 1,
    "Descriptive Analysis & Data Quality/Histograms": 1,
    "Descriptive Analysis & Data Quality/Outliers": 1,
    "Descriptive Analysis & Data Quality/Summary Statistics": 1,

    "Linear Regression/Goodness of fit": 1,
    "Linear Regression/Predictions, interpolation, extrapolation": 1,
    "Linear Regression/Scatter plot with model": 1,

    "Probability & Uncertainty/Relative Probability": 1,
    "Probability & Uncertainty/Z-Score Probability": 1,

    "Spreadsheet Foundations/Basic Calculations": 1,
    "Spreadsheet Foundations/Charting": 1,
    "Spreadsheet Foundations/Organizing Data": 1,
}

NUM_VERSIONS = 3

SEED = 1
random.seed(SEED)

# Supported image file extensions
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg"}


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def load_questions(folder_path):
    """
    Return all Markdown question files in a folder,
    excluding solution files (*-solution.md).
    """
    return [
        f for f in folder_path.glob("*.md")
        if not f.name.endswith("-solution.md")
    ]


def find_associated_images(question_file):
    """
    Find image files that share the same base name as the question.

    Example:
      carniverous-plants.md
      -> carniverous-plants-img.png
    """
    base_name = question_file.stem
    folder = question_file.parent

    return [
        f for f in folder.iterdir()
        if f.suffix.lower() in IMAGE_EXTENSIONS
        and f.name.startswith(base_name)
    ]


# -----------------------------
# EXAM GENERATION LOOP
# -----------------------------

for version in range(NUM_VERSIONS):

    exam_questions = []
    images_to_copy = set()  # Track images needed for this exam version

    for topic, num_questions in EXAM_STRUCTURE.items():

        # Build full path to the topic folder (supports nested folders)
        topic_folder = QUESTION_BANK / topic

        # Load valid question files
        all_questions = load_questions(topic_folder)

        # Randomly select questions
        chosen_questions = random.sample(all_questions, num_questions)

        for q in chosen_questions:
            exam_questions.append(q)

            # Collect associated images
            images = find_associated_images(q)
            images_to_copy.update(images)

    # Shuffle questions across topics
    random.shuffle(exam_questions)

    # -----------------------------
    # BUILD EXAM MARKDOWN TEXT
    # -----------------------------

    version_letter = chr(65 + version)
    exam_text = f"# Exam Version {version_letter}\n\n"

    for i, question_file in enumerate(exam_questions, start=1):
        exam_text += f"## Question {i}\n\n"
        exam_text += question_file.read_text() + "\n\n"

    output_file = OUTPUT_DIR / f"exam_{version_letter}.md"
    output_file.write_text(exam_text)

    # -----------------------------
    # COPY IMAGE FILES
    # -----------------------------

    for image_file in images_to_copy:
        destination = OUTPUT_DIR / image_file.name
        shutil.copy(image_file, destination)

    print(
        f"Generated {output_file} "
        f"with {len(images_to_copy)} associated images"
    )