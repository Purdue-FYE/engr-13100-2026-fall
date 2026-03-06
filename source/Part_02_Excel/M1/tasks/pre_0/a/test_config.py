from generic_grader.file import file_presence
from generic_grader.excel import data_match_reference, formulas_match_reference, formulas_exist, chart_metadata_match_reference, data_series_exists, data_series_match_reference
from generic_grader.utils.options import Options

DUE_DATE = None  # Unused because we don't accept late pre-class tasks.

SUB_MODULE = "ex1_pre_0"
REF_MODULE = "tests.ex1_pre_0_reference"
REQUIRED_FILES = (SUB_MODULE + "*.xlsx",)
TOTAL_POINTS = 5
file_set_up_options = Options(required_files=REQUIRED_FILES)

test_00_TestFilePresence = file_presence.build(
    Options(
        weight=TOTAL_POINTS/7,
        required_files=REQUIRED_FILES,
    )
)

test_01_TestDataSeriesExist = data_series_exists.build(
    Options(
        ref_module=REF_MODULE,
        sub_module=SUB_MODULE,
        entries=("F16", "F20"),
        weight=TOTAL_POINTS/7,
        sheet="Sheet1",
        series_require_formulas=True
    )
)

test_02_TestDataValues = data_series_match_reference.build(
    Options(ref_module=REF_MODULE, 
            sub_module=SUB_MODULE, 
            entries=("F16", "F20"),
            weight=TOTAL_POINTS/7,
            sheet="Sheet1"
        )
)


test_03_TestDataSeriesExist = data_series_exists.build(
    Options(
        ref_module=REF_MODULE,
        sub_module=SUB_MODULE,
        entries=("G24", "G30"),
        weight=TOTAL_POINTS/7,
        sheet="Sheet1",
        series_require_formulas=True
    )
)

test_04_TestDataSeriesExist = data_series_exists.build(
    Options(
        ref_module=REF_MODULE,
        sub_module=SUB_MODULE,
        entries=("H24", "H30"),
        weight=TOTAL_POINTS/7,
        sheet="Sheet1",
        series_require_formulas=True
    )
)

test_05_TestDataValues = data_series_match_reference.build(
    Options(ref_module=REF_MODULE,  
            sub_module=SUB_MODULE, 
            entries=("H24", "H30"),
            weight=TOTAL_POINTS/7,
            sheet="Sheet1",
            series_require_formulas=False
            )
)

test_06_ChartsMatchReference = chart_metadata_match_reference.build(
    Options(
        ref_module=REF_MODULE,
        sub_module=SUB_MODULE,
        entries=("Chart 1", "Chart 2"),
        sheet="Sheet1",
        weight=TOTAL_POINTS/7,
        chart_ratio=.15
    )
)