REPO = engr-13100-2026-fall
URL = https://purdue-fye.github.io/$(REPO)
PYTHON_BIN = $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

# Create a list of all exercise solutions and corresponding test_cases files by
# scanning through the tasks directories in each module.
modules = $(wildcard source/Part*/M*)
instructions = $(foreach dir,$(modules),$(wildcard $(dir)/tasks/*/*/*instructions.md))
solutions_Ex = $(foreach dir,$(modules),$(wildcard $(dir)/tasks/*/*/*solution.xlsx))
solutions_Py = $(foreach dir,$(modules),$(wildcard $(dir)/tasks/*/*/*solution.py))
solutions_MA = $(foreach dir,$(modules),$(wildcard $(dir)/tasks/*/*/*solution.m))
solutions = $(solutions_Ex) $(solutions_Py) $(solutions_MA)
test_cases = $(foreach dir,$(modules),$(wildcard $(dir)/tasks/*/*/*test_cases.py))
grader_files = $(wildcard grader/*)
quiz_files = $(wildcard source/quizzes/TTYK*.tex) $(wildcard source/quizzes/CQ*.tex)

grader_task_dirs = $(sort $(dir $(solutions_Py) $(solutions_Ex) $(solutions_MA)))
archives = $(addsuffix autograder.zip,$(subst source/,source/_build/graders/,$(grader_task_dirs)))

# Create a list of all sample output files to be generated for code-based tasks
# (.py and .m). Excel tasks keep solution.xlsx files, but do not produce
# sample_output artifacts.
#
# E.g. source/Part_3_Python/M1/tasks/ind_2/a/test_cases.py
#   -> source/_build/intermediate/Part_3_Python/M1/tasks/ind_2/a/solution.md
sample_output = $(foreach file,$(solutions_Py) $(solutions_MA),\
	$(subst source/,source/_build/intermediate/,\
		$(subst solution.,sample_output.,\
			$(subst .py,.md,\
				$(subst .m,.md,$(file))\
			)\
		)\
	)\
)

# Re-build only pages that are new/changed since last run.
default: $(sample_output)
	python3 source/utils/manage_deliverables.py
	jupyter-book build -W source
	rm -f source/_build/html/glue_factory.html source/_build/html/_sources/glue_factory.md
	touch source/_build/html/.nojekyll

# Re-build all pages.
all: $(sample_output)
	python3 source/utils/manage_deliverables.py
	PYTHONPATH="$(PWD)/source/_extensions:$(PYTHONPATH)" jupyter-book build -W --all source
	rm -f source/_build/html/glue_factory.html source/_build/html/_sources/glue_factory.md
	echo "View this site [here]($(URL))." > source/_build/html/README.md

graders: clean-graders grader/assignment_mapping.json
	$(PYTHON_BIN) source/generate_graders.py

# Publish to production site.
pub: all
	ghp-import --no-jekyll --push --no-history --remote $(REPO) ./source/_build/html

# Generate test case output
.SECONDEXPANSION:

%sample_output.md: \
	$$(filter $$(subst _build/intermediate/,,$$(subst sample_output.md,test_cases.py,$$@)), $(test_cases)) \
	$$(filter $$(subst _build/intermediate/,,$$(subst sample_output.md,solution.py,$$@)), $(solutions_Py)) \
	$$(filter $$(subst _build/intermediate/,,$$(subst sample_output.md,solution.m,$$@)), $(solutions_MA)) \
	$$(filter $$(subst _build/intermediate/,,$$(subst sample_output.md,instructions.md,$$@)), $(instructions)) \
	source/generate.py
	python3 source/generate.py $@

# All python3 files in exercise's test subdirectory are prerequisite.  Also include .png
# and .txt files, and all the grader specific files.
#
#  - % in the target matches the % in the prerequisites.
#  - $(@D)  is the directory part of the filename.
%autograder.zip : \
	$$(wildcard $(@D)/*.py) $$(wildcard $(@D)/*.png) $$(wildcard $(@D)/*.txt) $$(wildcard $(@D)/*.xlsx) $(grader_files)
	$(PYTHON_BIN) source/generate_graders.py "$(@D)"

grader/assignment_mapping.json: source/generate_assignment_mapping.py source/Part_00_Course_Resources/course_schedule/generate_schedule_assignments.py source/_toc.yml
	$(PYTHON_BIN) source/generate_assignment_mapping.py

# Make schedule document: 
schedule:
	python3 /workspaces/13100_content/source/Part_00_Course_Resources/generate_schedule.py
	make pub

# Generate teaching team list
teaching_team:
	python3 /workspaces/13100_content/source/Part_00_Course_Resources/generate_teachingteam.py
	make pub

# Clean up
clean:
	jupyter-book clean source/

clean-all:
	jupyter-book clean source/ --all

clean-graders:
	# Remove all built grader files
	rm -rf source/_build/graders
