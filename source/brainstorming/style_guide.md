# Style Guide for Website Modules

## 0_overview.md - Module Landing Page

### How to Anchor
```
(TOPIC:MOD_NUM:Overview)=
# Page Name Here
```
So an example would be:
```
(EX:M1:Overview)=
# Spreadsheet Foundations
```
Use the following topic abbreviations:
- EX for Excel
- PY for Python
- MA for MATLAB
- AI for Artificial Intelligence
- PD for Professional Development
- TP for Team Project


### Headers and Content
This module [summary or introduction to content...]

```{rubric} Topics Covered
```
- Topic
- Topic

```{rubric} Skills and Learning Objectives
```
At the end of this module, you will be able to:

- Skills
- Skills

These skills are directly connected to the following Learning Objectives:

{{PR01}}

## 1_pre-class_overview.md - PC Landing Page for the Module
### How to Anchor
```
(TOPIC:MOD_NUM:pre-class)=
# Pre-Class Assignments
```

### Headers and Content
The Pre-Class Materials (PCMs) and Pre-Class Activities (PCAs) are your **core learning materials** in ENGR 131. Completing them **before each class session** ensures you’re ready for in-class discussions, activities, and assignments.

```{rubric} What to Expect
```
- Watch short instructional videos to learn key concepts and prepare for class.
- Read and review the accompanying notes, examples, or scripts provided in the materials.
- Complete the associated pre-class activities (PCAs) to check your understanding and reinforce learning.
- Materials are available anytime — revisit them as needed to deepen your understanding.

```{rubric} Materials and Activities for this Module
```

```{tableofcontents}
```

```{rubric} Helpful [TOPIC] Resources
```
- resource
- resource

## 1.1_materials.md - Pre-Class Materials Page
### How to Anchor
```
(TOPIC:MOD_NUM:pre-class-mats)=
# PCMs: Module Name
```
The
### Content Guidelines
Each page should start with "These pre-class materials introduce..." and a quick summary of the skills on this page.

Then start at H2 and organize the topics appropriately.

#### Admonitions

Example:

```{admonition} TITLE
:class: note
Content goes here
```

|Class | Symbol | Color | Use Case |
| ------- | ------- | ------- | ------ |
| note | "i" in a circle | blue | providing additional information, shortcuts, or resources |
| tip | lightbulb | green | downloading practice files <br>CFU questions <br>Hints |
| important | "!" in a circle | orange | highlight important/key information |

##### CFU Formatting
```
     ```{admonition} Check for Understanding
    :class: tip

    QUESTION

    :::{dropdown} Show Answer
    **Correct Answer: LETTER** or **Correct Answer:** VALUE/EXPLANATION

    FEEDBACK
    :::
    ```
```

## /tasks/pre_0/a/instructions.md - PCA Instructions page
### How to Anchor
```
(TOPIC:MOD_NUM:PCA#)=
# PCA: Title
```

## 2_in-class_overview.md - In-Class Activities
### How to Anchor
```
(TOPIC:MOD_NUM:in-class)=
# In-Class Activities
```

### Headers and Content
**In-Class Activities (ICAs)** are where you apply what you’ve learned in the Pre-Class Materials (PCMs) and Pre-Class Activities (PCAs). During class, you’ll work through problems, collaborate with your team, and practice key skills to help you prepare for assignments and exams.

```{rubric} Activities for this Module
```

```{tableofcontents}
```

## /in-class/ICA_1/instructions.md - ICA instructions page

### How to Anchor
To anchor the lower level pages, use:
```
(TOPIC:MOD_NUM:ICA#)=
# ICA: Title
```
Replace # with the ICA number in the file structure



## 3_assignments_overview.md - Assignments Landing Page
### How to Anchor
```
(TOPIC:MOD_NUM:assignments)=
# Assignments
```

### Headers and Content

```{rubric} In these assignments, you will:
```
- Skill
- Skill
- Skill

```{rubric} Learning Objectives
```
{{PR01}}

```{rubric} Assignments for this Module
```

```{tableofcontents}
```

## /tasks/1/a/instructions.md - Assignment instructions page
### How to Anchor
To anchor the lower level pages, use:
```
(TOPIC:MOD_NUM:A#)=
# TOPIC: Title
```
Replace # with the TOPIC with the corresponding abbreviation and # with the number in the file structure

Use the following topic abbreviations:
- EX for Excel
- PY for Python
- MA for MATLAB
- AI for Artificial Intelligence
- TP for Team Project
- TM for Teaming
- CAT for CATME

### Headers and Content
