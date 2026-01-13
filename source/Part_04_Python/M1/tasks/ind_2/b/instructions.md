---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
myst:
  substitutions:
    label_srs: 'eq:py1:series'
    label_prl: 'eq:py1:parallel'

    # Variations: place selected variation last

    ## Inductor
    element: "inductor"
    measurement: "inductance"
    intro: >
      You may recall from your high school physics class that an inductor is an
      electrical component that stores energy in a magnetic field when electrical
      current flows through it.  Inductors are commonly used in electronic circuits to
      filter signals, store energy, and manage current flow.  The value of an inductor's
      inductance is given by {math}`L` (with unit Henries {math}`[\henry]`).

    func_srs_md: >
      L_\text{total} = L_1 + L_2 + \cdots + L_n
    func_srs_py: >
      E1 + E2
    func_prl_md: >
      \frac{1}{L_\text{total}} = \frac{1}{L_1} + \frac{1}{L_2} + \cdots + \frac{1}{L_n}
    func_prl_py: >
      1 / (1 / E1 + 1 / E2)
    unit_hint: ""
    fixed_value_md: >
      {math}`\qty{2e^2\sqrt[]{3}}{\milli\henry}` where {math}`e` is Euler's number
    fixed_value_py: >
      2 * math.exp(2) * math.sqrt(3)
    unit: "mH"


    ## Resistor  Fall 2024
    element: "resistor"
    measurement: "resistance"
    intro: >
      You may recall from your high school physics class that a resistor is an
      electrical component that reduces the flow of current through a circuit.  Most
      generally, a resistor turns electrical current into a different type of energy,
      such as noise, light, or heat.  Anything that draws current from the circuit, such
      as a light, can be modeled as having a resistance value {math}`R` (with unit Ohms
      {math}`[\ohm]`).
    func_srs_md: >
      R_\text{total} = R_1 + R_2 + \cdots + R_n
    func_srs_py: >
      E1 + E2
    func_prl_md: >
      \frac{1}{R_\text{total}} = \frac{1}{R_1} + \frac{1}{R_2} + \cdots + \frac{1}{R_n}
    func_prl_py: >
      1 / (1 / E1 + 1 / E2)
    unit_hint: >
      - Entering {python}`\u2126` in a string will produce the {math}`\Omega` symbol.
    fixed_value_md: >
      {math}`\qty{e^2\sqrt[]{7}}{\ohm}` where {math}`e` is Euler's number
    fixed_value_py: >
      math.exp(2) * math.sqrt(7)
    unit: "k\u2126"


    ## Capacitor  Fall 2025
    element: "capacitor"
    measurement: "capacitance"
    intro: >
      You may recall from your high school physics class that a capacitor is an
      electrical component that stores energy in an electric field.  Capacitors are
      commonly used in electronic circuits to store and release energy, filter signals,
      and stabilize voltage levels.  The value of a capacitor's capacitance is given by
      {math}`C` (with unit Farads {math}`[\farad]`).
    func_srs_md: >
      \frac{1}{C_\text{total}} = \frac{1}{C_1} + \frac{1}{C_2} + \cdots + \frac{1}{C_n}
    func_srs_py: >
      1 / (1 / E1 + 1 / E2)
    func_prl_md: >
      C_\text{total} = C_1 + C_2 + \cdots + C_n
    func_prl_py: >
      E1 + E2
    unit_hint: >
      - Entering {python}`\u03bc` in a string will produce the {math}`\mu` symbol.
    fixed_value_md: >
      {math}`\qty{e^3\sqrt[]{5}}{\mu\farad}` where {math}`e` is Euler's number
    fixed_value_py: >
      math.exp(3) * math.sqrt(5)
    unit: "\u03bcF"
---
```{include} /macros.md
```

(mod:py1_ind_task_2)=
# Individual Task 2


## Learning Objectives

Create and execute simple scripts comprised of basic {program}`Python` concepts; Output
data from a script to the screen in {program}`Python`; Apply this course's programming
standards in development of {program}`Python` scripts; Modularize and comment code in
{program}`Python` for readability and reusability.


## Task Instructions

{{ intro }}
In circuits with many components, we can calculate an equivalent {{ measurement }} for
the entire circuit using the individual {{ measurement }}s of each component.  Knowing
this equivalent {{ measurement }} can make calculating other properties of the circuit
much easier.

We frequently encouter two electrical circuit topologies: series and parallel.  For each
type, one can calculate a total {{ measurement }} for the entire circuit, but the two
are calculated differently.  The total {{ measurement }} for series {{ element }}s is
calculated as shown in {eq}`eq:py1:series`, while that for parallel {{ element }}s is
shown in {eq}`eq:py1:parallel`.

{{ "```{}\n:label: {}\n{}{}\n```".format("{math}", label_srs, func_srs_md, "\\quad\\text{(Series)}") }}
{{ "```{}\n:label: {}\n{}{}\n```".format("{math}", label_prl, func_prl_md, "\\quad\\text{(Parallel)}") }}

Create a program to calculate the total {{ measurement }} of two {{ element }}s arranged
in series and in parallel. The program should output the results for both series AND
parallel calculations.  The value of the first {{ element }}'s {{ measurement }} should
be an input from the user, while the second {{ element }}'s {{ measurement }} should be
hardcoded as {{ fixed_value_md }}.

A flowchart illustrating your program's logic should be created and saved in a PDF file
named {glue:text}`../../../3_ind_assignments.md::deliverable_py1_ind_2_pdf:`.  Start
your {program}`Python` script from {download}`ENGR131_Python_Template.py
</Part_04_Python/ENGR131_Python_Template.py>` and save it as
{glue:text}`../../../3_ind_assignments.md::deliverable_py1_ind_2_py:`.  Use the sample
output section below to verify that your program outputs correct values.

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M1/tasks/ind_2/b/sample_output.md
```

```{admonition} Hints
:class: hint

- Use f-strings to format your output.

- Line your output values up by setting a width in your f-string.  For example,
  {python}`f"{value:10.2f}"` will format the value to have a width of {math}`10`
  characters and {math}`2` decimal places.

{{ unit_hint }}
```

```{list-table} Deliverables
:class: deliverables
:name: tab:Py:M1:individual_2_deliverables
:header-rows: 1

* - Deliverables
  - Description

* - {glue:text}`../../../3_ind_assignments.md::deliverable_py1_ind_2_pdf:`
  - Flowchart(s) for this task.

* - {glue:text}`../../../3_ind_assignments.md::deliverable_py1_ind_2_py:`
  - Your completed {program}`Python` code.
```