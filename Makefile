REPO = engr-13100-2026-fall
URL = https://purdue-fye.github.io/$(REPO)

# Create a list of all sample output files to be generated, by scanning through
# the test_cases, changing source to source/_build/intermediate, and changing
# the file extension from .py to .md.
#
# E.g. source/Part_3_Python/M1/tasks/ind_2/a/test_cases.py
#   -> source/_build/intermediate/Part_3_Python/M1/tasks/ind_2/a/solution.md
sample_output = $(foreach file,$(solutions),\
	$(subst source/,source/_build/intermediate/,\
		$(subst solution.,sample_output.,\
			$(subst .py,.md,\
				$(subst .m,.md,$(file))\
			)\
		)\
	)\
)

# Re-build only pages that are new/changed since last run.
default:
	PYTHONPATH="$(PWD)/source/_extensions:$(PYTHONPATH)" jupyter-book build -W source
	touch source/_build/html/.nojekyll


# Re-build all pages.
all:
	PYTHONPATH="$(PWD)/source/_extensions:$(PYTHONPATH)" jupyter-book build -W --all source
	echo "View this site [here]($(URL))." > source/_build/html/README.md

# Publish to production site.
pub: all
	ghp-import --no-jekyll --push --no-history --remote $(REPO) ./source/_build/html

# Clean up
clean:
	jupyter-book clean source/

clean-all:
	jupyter-book clean source/ --all