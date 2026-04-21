from generic_grader.file import file_presence
from generic_grader.output import output_values_match_reference
from generic_grader.utils.options import Options

# OPTIONS --> A CONFIGURATION OBJECT USED TO PASS PARAMETERS ( weight, filenames, module names, etc.) TO TEST BUILDERS

DUE_DATE = None  # Unused because we don't accept late pre-class tasks.

SUB_MODULE = "py1_pre_1"
REF_MODULE = "py1_pre_1_reference" # IMPORT PATH TO REFERENCE SOLUTION
REQUIRED_FILES = (SUB_MODULE + "*.py",)
file_set_up_options = Options(required_files=REQUIRED_FILES) # FILES MUST EXIST BEFORE RUNNING TESTS

# FILE PRESENCE TEST ("py_1_pre_1*.py")
# IF TEST FAILS, STOP ALL FURTHER TESTING
test_00_TestFilePresence = file_presence.build(
    Options(
        weight=2, # test is worth 2 points
        required_files=REQUIRED_FILES,
    )
)

""" OUTPUT MATCHING TEST:
1. IMPORT THE STUDENT MODULE
2. IMPORT THE REFERENCE MODULE
3. CALL THE MAIN FUNCTION (DRIVER FILE)
4. COMPARE OUTPUT FOR SPECIFIC LINES (1-9)

"""
test_01_TestOutputValues = output_values_match_reference.build(
    Options(
        weight=1, 
        ref_module=REF_MODULE, 
        sub_module=SUB_MODULE,
        entries=("2", "6"), # INPUTS FOR LINES 1-2
        obj_name="main", 
        line_n=line)
    for line in (1, 2, 3, 4, 5, 6, 7, 8, 9)
)