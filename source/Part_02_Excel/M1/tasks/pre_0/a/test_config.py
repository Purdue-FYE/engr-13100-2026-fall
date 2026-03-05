from generic_grader.file import file_presence
from generic_grader.excel import data_match_reference
from generic_grader.excel import formulas_exist
from generic_grader.utils.options import Options

DUE_DATE = None  # Unused because we don't accept late pre-class tasks.

SUB_MODULE = "ex1_pre_0"
REF_MODULE = "tests.ex1_pre_0_reference"
REQUIRED_FILES = (SUB_MODULE + "*.xlsx",)
TOTAL_POINTS = 5
file_set_up_options = Options(required_files=REQUIRED_FILES)

test_00_TestFilePresence = file_presence.build(
    Options(
        weight=2,
        required_files=REQUIRED_FILES,
    )
)

test_01_TestDataValues = data_match_reference.build(
    Options(ref_module=REF_MODULE, 
            sub_module=SUB_MODULE, 
            entries=("F16", "F20"),
            weight=3
            kwargs={"sheet": "Sheet1"})
    
)

test_02_TestFormulasExist = formulas_exist.build(
    Options(
        ref_module=REF_MODULE,
        sub_module=SUB_MODULE,
        entries=("F16", "F20"),
        kwargs={"sheet": "Sheet1"}
    )
)