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

import pandas as pd
from myst_nb import glue
from IPython.display import Markdown, display

# Read the CSV containing deliverable information
csv_path = 'engr131_student_deliverables_list.csv'
df = pd.read_csv(csv_path)

# Iterate through the DataFrame to glue variables
for index, row in df.iterrows():
    # Construct a unique key based on module, mode, task, and deliverable number
    # Example key base: py1_team_1_1
    key_parts = [
        str(row['module']),
        str(row['mode']),
        str(row['task number']),
        str(row['deliverable number'])
    ]
    base_key = "_".join(key_parts)

    # Glue the deliverable name (filename)
    # Usage in markdown: {glue:text}`deliverable_py1_team_1_1_name`
    glue(f"deliverable_{base_key}_name", row['deliverable name'], display=False)

    # Glue the deliverable description
    # Usage in markdown: {glue:text}`deliverable_py1_team_1_1_desc`
    glue(f"deliverable_{base_key}_desc", row['deliverable description'], display=False)
```

```{code-cell} ipython3
:tags: ["remove-input"]

# This cell generates a table of all deliverables defined in the CSV
# to verify that they have been loaded correctly.

# Dynamically generate the list-table markdown
table_md = """
```{list-table} Deliverables
:class: deliverables
:name: tab:dynamic_deliverables
:header-rows: 1
:widths: 20 40 40

* - Key Base
  - Deliverable Name
  - Description
"""

for index, row in df.iterrows():
    key_parts = [
        str(row['module']),
        str(row['mode']),
        str(row['task number']),
        str(row['deliverable number'])
    ]
    base_key = "_".join(key_parts)
    table_md += f"* - `{base_key}`\n  - {{glue:text}}`deliverable_{base_key}_name`\n  - {{glue:text}}`deliverable_{base_key}_desc`\n"

table_md += "```"

display(Markdown(table_md))