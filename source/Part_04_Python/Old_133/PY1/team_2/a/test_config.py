import random as r

from generic_grader.file import file_presence
from generic_grader.output import (
    output_lines_match_reference,
    output_values_match_reference,
)
from generic_grader.style import comments, docstring, program_length
from generic_grader.utils.options import Options

DUE_DATE = "2025-09-12 10:00 PM"

REF_MODULE = "tests.py1_team_2_reference"
SUB_MODULE = "py1_team_2"
REQUIRED_FILES = (SUB_MODULE + "*.py",)
file_set_up_options = Options(required_files=REQUIRED_FILES)

test_00_TestFilePresence = file_presence.build(
    Options(
        weight=0.5,
        required_files=REQUIRED_FILES,
    )
)

cases = (
    (5,),
    (r.randint(100, 1000),),
)

test_01_TestOutputValues = output_values_match_reference.build(
    Options(
        ref_module=REF_MODULE,
        sub_module=SUB_MODULE,
        obj_name="main",
        entries=case,
        line_n=line,
    )
    for case in cases
    for line in (2, 3, 4, 5)
)

test_02_TestOutputLines = output_lines_match_reference.build(
    Options(
        ref_module=REF_MODULE,
        sub_module=SUB_MODULE,
        obj_name="main",
        entries=cases[1],
    )
)

test_03_TestDocstring = docstring.build(
    Options(ref_module=REF_MODULE, sub_module=SUB_MODULE)
)

test_04_TestCommentLength = comments.build(
    Options(
        ref_module=REF_MODULE,
        sub_module=SUB_MODULE,
        hint="Check the volume of comments in your code.",
    )
)

test_05_TestProgramLength = program_length.build(
    Options(ref_module=REF_MODULE, sub_module=SUB_MODULE)
)
