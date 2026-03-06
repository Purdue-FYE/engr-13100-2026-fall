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
```{include} /macros.md
```

(Py:M3:py3_pre_2_b)=
# Pre-Class Activity #X: Looping Structures

## Learning Objectives

- PR01: Programming Standards
- PR02: Data Storage
- PR03: Calculations
- PR04: Modular Programming
- PR05: Code Structures
- PR06: Translate Program Descriptions
- PR07: Test cases & Tracking
- PR08: Debugging

## Files Needed

<!-- Download the {program}`Python` template {download}`ENGR131_Python_Template.py </Part_04_Python/ENGR131_Python_Template.py>` and save it as {glue:text}`../../../../../glue_factory.md::py3_pre_2_py:`. -->

## Activity Instructions & Submission

The flowchart below includes a for loop, as indicated by the rectangle with a dashed line in the figure.

```{mermaid}
flowchart LR
 subgraph WhileLoop["While Loop (t &lt; 2)"]
        H{"t &lt; 2?"}
        G["t = 0"]
        I["x = x + 1"]
        J["Print \Incremented x in while loop\"]
        K["t = t + 1"]
  end
 subgraph IfBlock["If x &lt; 18"]
        L{"x &lt; 18?"}
        M["x = x + 1"]
        N["Print \Incremented x\"]
  end
    A(["Start"]) --> B[/"Input x"/]
    B --> C["Print \Start: x = x\"]
    C --> D["i = 0"]
    D --> E{"i &lt; 100?"}
    G --> H
    H -- Yes --> I
    I --> J
    J --> K
    K --> H
    L -- Yes --> M
    M --> N
    E -- Yes --> F["Print \Pass i+1: x = x\"]
    F --> G
    H -- No --> L
    N --> Q["i = i + 1"]
    Q --> E
    E L_E_O_0@-- No --> O["Print \Number of iterations: i+1\"]
    L -- No --> O
    O --> P(["End"])

    L_E_O_0@{ curve: linear }
```

Review the flowchart and use it to write a Python script. Use the sample output section below to verify that your program outputs correct values.

% Automatically generated Sample Output section.
```{include} /_build/intermediate/Part_04_Python/M3/tasks/pre_2/a/sample_output.md
```

## Deliverables

<!-- Submit your {program}`Python` file {glue:text}`../../../../../glue_factory.md::py3_pre_2_py:` to (INSERT ASSIGNMENT NAME) on Gradescope. -->