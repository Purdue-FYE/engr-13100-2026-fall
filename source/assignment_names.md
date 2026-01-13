---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
:tags: ["remove-cell"]

from myst_nb import glue

mnum = "py1_team"

glue("deliverable_py1_team_1_pdf", mnum+"_1_teamnumber.pdf")
glue("deliverable_py1_team_1_py", mnum+"_1_teamnumber.py")

glue("deliverable_py1_team_2_part_a_pdf", mnum+"_2_part_a_teamnumber.pdf")
glue("deliverable_py1_team_2_pdf", mnum+"_2_teamnumber.pdf")
glue("deliverable_py1_team_2_py", mnum+"_2_teamnumber.py")

glue("deliverable_py1_team_3_pdf", mnum+"_3_teamnumber.pdf")
glue("deliverable_py1_team_3_py", mnum+"_3_teamnumber.py")
```

```{code-cell} ipython3

from myst_nb import glue
from IPython.display import Markdown, display

assignment_dict = {
    "py1_team1_1": "py1_team_1_teamnumber.pdf",
    "py1_team1_2": "py1_team_1_teamnumber.py",

    "py1_team2_1": "py1_team_2_part_a_teamnumber.pdf",
    "py1_team2_2": "py1_team_2_teamnumber.pdf",
    "py1_team2_3": "py1_team_2_teamnumber.py",

    "py1_team3_1": "py1_team_3_teamnumber.pdf",
    "py1_team3_2": "py1_team_3_teamnumber.py",
}

for key, value in assignment_dict.items():
    glue("deliverable_"+key, value)

# Dictionary mapping assignment keys to descriptions
descriptions = {
    "py1_team1_1": "Team 1 PDF Deliverable",
    "py1_team1_2": "Team 1 Python Script",
    "py1_team2_1": "Team 2 Part A PDF",
    "py1_team2_2": "Team 2 PDF Deliverable",
    "py1_team2_3": "Team 2 Python Script",
    "py1_team3_1": "Team 3 PDF Deliverable",
    "py1_team3_2": "Team 3 Python Script",
}

# Define the filter string for the specific assignment (e.g., "py1_team1")
assignment_filter = "py1_team1"

# Dynamically generate the list-table markdown
table_md = """
```{list-table} Deliverables
:class: deliverables
:name: tab:dynamic_deliverables
:header-rows: 1

* - Deliverables
  - Description
"""

for key in assignment_dict:
    if assignment_filter in key:
        glue_key = f"deliverable_{key}"
        desc = descriptions.get(key, "Description not provided")
        table_md += f"* - {{glue:text}}`{glue_key}`\n  - {desc}\n"

table_md += "```"

display(Markdown(table_md))