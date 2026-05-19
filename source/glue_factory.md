---
orphan: true
mystnb:
    execution_mode: force
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Glue Factory

Auto-generated glue key definitions for deliverable filenames.

```{code-cell} python3
:tags: [remove-cell]

from myst_nb import glue
import pathlib

# GLUE FACTORY: Auto-generated variables
# DO NOT EDIT THIS CELL MANUALLY
#
# Instructor front-matter template in assignment markdown files:
#
# ---
# deliverables:
#   - report_pdf
#   - appendix_pdf
#   - analysis_py
#   - data_xlsx
# ---
#
# Also supported:
# deliverables:
#   - key: report_pdf
#   - label: analysis
#     ext: py

# ex1_pre_1
glue('ex1_pre_1_powerdatavalues_pdf', 'ex1_pre_1_powerdatavalues_username.pdf', display=False)
glue('ex1_pre_1_powerdataformulas_pdf', 'ex1_pre_1_powerdataformulas_username.pdf', display=False)

# ex1_ica_1
glue('ex1_ica_1_powerdatavalues_pdf', 'ex1_ica_1_powerdatavalues_username.pdf', display=False)
glue('ex1_ica_1_powerdataformulas_pdf', 'ex1_ica_1_powerdataformulas_username.pdf', display=False)

# ex2_pre_1
glue('ex2_pre_1_pdf', 'ex2_pre_1_username.pdf', display=False)
glue('ex2_pre_1_py', 'ex2_pre_1_username.py', display=False)
glue('ex2_pre_1_xlsx', 'ex2_pre_1_username.xlsx', display=False)
glue('ex2_pre_1_zip', 'ex2_pre_1_username.zip', display=False)

# ex2_pre_2
glue('ex2_pre_2_pdf', 'ex2_pre_2_username.pdf', display=False)
glue('ex2_pre_2_py', 'ex2_pre_2_username.py', display=False)
glue('ex2_pre_2_xlsx', 'ex2_pre_2_username.xlsx', display=False)
glue('ex2_pre_2_zip', 'ex2_pre_2_username.zip', display=False)

# ex2_ica_1
glue('ex2_ica_1_powerdatavalues_pdf', 'ex2_ica_1_powerdatavalues_username.pdf', display=False)
glue('ex2_ica_1_powerdataformulas_pdf', 'ex2_ica_1_powerdataformulas_username.pdf', display=False)

# ex2_1
glue('ex2_1_powerdatavalues_pdf', 'ex2_1_powerdatavalues_username.pdf', display=False)
glue('ex2_1_powerdataformulas_pdf', 'ex2_1_powerdataformulas_username.pdf', display=False)

# ex3_pre_1
glue('ex3_pre_1_pdf', 'ex3_pre_1_username.pdf', display=False)
glue('ex3_pre_1_py', 'ex3_pre_1_username.py', display=False)
glue('ex3_pre_1_xlsx', 'ex3_pre_1_username.xlsx', display=False)
glue('ex3_pre_1_zip', 'ex3_pre_1_username.zip', display=False)

# ex3_ica_1
glue('ex3_ica_1_powerdatavalues_pdf', 'ex3_ica_1_powerdatavalues_username.pdf', display=False)
glue('ex3_ica_1_powerdataformulas_pdf', 'ex3_ica_1_powerdataformulas_username.pdf', display=False)

# ex4_pre_1
glue('ex4_pre_1_pdf', 'ex4_pre_1_username.pdf', display=False)
glue('ex4_pre_1_py', 'ex4_pre_1_username.py', display=False)
glue('ex4_pre_1_xlsx', 'ex4_pre_1_username.xlsx', display=False)
glue('ex4_pre_1_zip', 'ex4_pre_1_username.zip', display=False)

# ex4_ica_1
glue('ex4_ica_1_powerdatavalues_pdf', 'ex4_ica_1_powerdatavalues_username.pdf', display=False)
glue('ex4_ica_1_powerdataformulas_pdf', 'ex4_ica_1_powerdataformulas_username.pdf', display=False)

# ex4_1
glue('ex4_1_powerdatavalues_pdf', 'ex4_1_powerdatavalues_username.pdf', display=False)
glue('ex4_1_powerdataformulas_pdf', 'ex4_1_powerdataformulas_username.pdf', display=False)

# py1_pre_1
glue('py1_pre_1_pdf', 'py1_pre_1_username.pdf', display=False)
glue('py1_pre_1_py', 'py1_pre_1_username.py', display=False)
glue('py1_pre_1_xlsx', 'py1_pre_1_username.xlsx', display=False)
glue('py1_pre_1_zip', 'py1_pre_1_username.zip', display=False)

# py1_ica_1
glue('py1_ica_1_powerdatavalues_pdf', 'py1_ica_1_powerdatavalues_username.pdf', display=False)
glue('py1_ica_1_powerdataformulas_pdf', 'py1_ica_1_powerdataformulas_username.pdf', display=False)

# py1_ind_1
glue('py1_ind_1_report_pdf', 'py1_ind_1_report_username.pdf', display=False)
glue('py1_ind_1_py', 'py1_ind_1_username.py', display=False)

# py2_pre_1
glue('py2_pre_1_pdf', 'py2_pre_1_username.pdf', display=False)
glue('py2_pre_1_py', 'py2_pre_1_username.py', display=False)
glue('py2_pre_1_xlsx', 'py2_pre_1_username.xlsx', display=False)
glue('py2_pre_1_zip', 'py2_pre_1_username.zip', display=False)

# py2_pre_2
glue('py2_pre_2_pdf', 'py2_pre_2_username.pdf', display=False)
glue('py2_pre_2_py', 'py2_pre_2_username.py', display=False)
glue('py2_pre_2_xlsx', 'py2_pre_2_username.xlsx', display=False)
glue('py2_pre_2_zip', 'py2_pre_2_username.zip', display=False)

# py2_ica_1
glue('py2_ica_1_py', 'py2_ica_1_username.py', display=False)

# py2_ind_1
glue('py2_ind_1_pdf', 'py2_ind_1_username.pdf', display=False)
glue('py2_ind_1_py', 'py2_ind_1_username.py', display=False)
glue('py2_ind_1_xlsx', 'py2_ind_1_username.xlsx', display=False)
glue('py2_ind_1_zip', 'py2_ind_1_username.zip', display=False)

# py3_pre_1
glue('py3_pre_1_pdf', 'py3_pre_1_username.pdf', display=False)
glue('py3_pre_1_py', 'py3_pre_1_username.py', display=False)
glue('py3_pre_1_xlsx', 'py3_pre_1_username.xlsx', display=False)
glue('py3_pre_1_zip', 'py3_pre_1_username.zip', display=False)

# py3_pre_2
glue('py3_pre_2_pdf', 'py3_pre_2_username.pdf', display=False)
glue('py3_pre_2_py', 'py3_pre_2_username.py', display=False)
glue('py3_pre_2_xlsx', 'py3_pre_2_username.xlsx', display=False)
glue('py3_pre_2_zip', 'py3_pre_2_username.zip', display=False)

# py3_ica_1
glue('py3_ica_1_powerdatavalues_pdf', 'py3_ica_1_powerdatavalues_username.pdf', display=False)
glue('py3_ica_1_powerdataformulas_pdf', 'py3_ica_1_powerdataformulas_username.pdf', display=False)

# py3_ind_1
glue('py3_ind_1_pdf', 'py3_ind_1_username.pdf', display=False)
glue('py3_ind_1_py', 'py3_ind_1_username.py', display=False)
glue('py3_ind_1_xlsx', 'py3_ind_1_username.xlsx', display=False)
glue('py3_ind_1_zip', 'py3_ind_1_username.zip', display=False)

# py4_pre_1
glue('py4_pre_1_pdf', 'py4_pre_1_username.pdf', display=False)
glue('py4_pre_1_py', 'py4_pre_1_username.py', display=False)
glue('py4_pre_1_xlsx', 'py4_pre_1_username.xlsx', display=False)
glue('py4_pre_1_zip', 'py4_pre_1_username.zip', display=False)

# py4_pre_2
glue('py4_pre_2_pdf', 'py4_pre_2_username.pdf', display=False)
glue('py4_pre_2_py', 'py4_pre_2_username.py', display=False)
glue('py4_pre_2_xlsx', 'py4_pre_2_username.xlsx', display=False)
glue('py4_pre_2_zip', 'py4_pre_2_username.zip', display=False)

# py4_ica_1
glue('py4_ica_1_powerdatavalues_pdf', 'py4_ica_1_powerdatavalues_username.pdf', display=False)
glue('py4_ica_1_powerdataformulas_pdf', 'py4_ica_1_powerdataformulas_username.pdf', display=False)

# py4_ind_1
glue('py4_ind_1_pdf', 'py4_ind_1_username.pdf', display=False)
glue('py4_ind_1_py', 'py4_ind_1_username.py', display=False)
glue('py4_ind_1_xlsx', 'py4_ind_1_username.xlsx', display=False)
glue('py4_ind_1_zip', 'py4_ind_1_username.zip', display=False)

# py5_pre_1
glue('py5_pre_1_pdf', 'py5_pre_1_username.pdf', display=False)
glue('py5_pre_1_py', 'py5_pre_1_username.py', display=False)
glue('py5_pre_1_xlsx', 'py5_pre_1_username.xlsx', display=False)
glue('py5_pre_1_zip', 'py5_pre_1_username.zip', display=False)

# py5_ica_1
glue('py5_ica_1_powerdatavalues_pdf', 'py5_ica_1_powerdatavalues_username.pdf', display=False)
glue('py5_ica_1_powerdataformulas_pdf', 'py5_ica_1_powerdataformulas_username.pdf', display=False)

# py5_ind_1
glue('py5_ind_1_pdf', 'py5_ind_1_username.pdf', display=False)
glue('py5_ind_1_py', 'py5_ind_1_username.py', display=False)
glue('py5_ind_1_xlsx', 'py5_ind_1_username.xlsx', display=False)
glue('py5_ind_1_zip', 'py5_ind_1_username.zip', display=False)

```
