from generic_grader.file import file_presence
from generic_grader.output import output_values_match_reference
from generic_grader.utils.options import Options

DUE_DATE = "2025-09-12 10:00 PM"

REF_MODULE = "tests.py1_team_1_reference"
SUB_MODULE = "py1_team_1"
REQUIRED_FILES = (SUB_MODULE + "*.py",)
file_set_up_options = Options(required_files=REQUIRED_FILES)

test_00_TestFilePresence = file_presence.build(Options(required_files=REQUIRED_FILES))

test_01_TestOutputValues = output_values_match_reference.build(
    Options(ref_module=REF_MODULE, sub_module=SUB_MODULE, line_n=line)
    for line in (1, 2, 3)
)