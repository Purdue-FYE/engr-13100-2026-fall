---
title: Design Project Technical Report
subtitle: "ENGR 131 Team Project: The Martian Greenhouse"
lang: en-US
---

::: {custom-style="Project Title"}
[Project Title]
:::

[Insert an image related to the problem or your solution, and add alternative text that
describes the image.]

::: {custom-style="Title Page"}
Prepared for [client name]

Section [number], Team [number]

[Names of all contributing team members]

[Date]
:::

[Replace each bracketed placeholder on this page with your own information (PC01,
PC05).]

# How to Use This Template {#how-to-use-this-template}

[Delete this section, including its table, before your first submission.]

[Your team builds this report across the five milestones of the project. Each section
begins by naming the milestone in which you draft it. Later milestones also revise
earlier sections, because new evidence changes the design.]

[Text in square brackets is guidance or a placeholder. Replace each placeholder with
your own work, and delete all guidance before each submission. Codes such as (PS01) name
the course learning objective that a section assesses. The codes are for the grading
team, and you do not need to write about them.]

[Use the built-in heading styles for every heading you add, so that the Table of
Contents and screen readers can find it. Give every table and figure a numbered caption,
and add alternative text to every image, chart, and drawing.]

[Table A lists the sections you draft and revise at each milestone. The Design Process
page on the course website pairs the same schedule with the design stage of each
milestone.]

: Table A. Report sections by milestone

| Checkpoint | Sections you draft | Sections you revise |
|-------------|------------------------------------------|------------------------------------------|
| TP1 (M1) | II. Team Member Roles; III. Problem Scoping | None |
| TP2 (M2) | IV. Idea Generation; V. Thought Experiments | III. Problem Scoping |
| TP3 (M3) | VI. Iteration #1; VII.a Testing Protocol; VII.b Prototypes; VII.d Weighted Decision Matrix (predicted scores) | III.b Design Criteria and Constraints; IV. Idea Generation (narrow to finalists) |
| TP4 (M4) | VII.c Test Results; VIII. Iteration #2; IX.a Detailed Design; IX.b Data on the Final Solution | VI. Iteration #1; VII.d Weighted Decision Matrix (add measured results) |
| TP5 (M5) | I. Executive Summary; IX.c Novel Aspects; IX.d Trade-off Decisions and Limitations; IX.e Lessons Learned; X. References | All sections, for a reader who was not part of the project |

\[In this project, you design the greenhouse system in your report, including its
sensors and its control approach. You also select the glazing and heater for GHU-2 from
a menu, size its battery, and write the control software. Because of this hybrid scope,
three terms in this template have specific meanings.

- **Prototype:** a candidate design, which pairs a hardware selection with a control
  strategy. It is not a physical model.
- **Test:** run the simulation on the hardware of a prototype and read its metrics.
- **Build:** write your controller code and run it in the simulation on the hardware
  your team declared.]

# I. Executive Summary

\[Draft this section last, in M5 (TP5). An executive summary is a one-page description
of the project that a reader can understand without the rest of the report (PC05).
Include each of the following items.

- The problem
- Your design requirements (criteria and constraints)
- The control solution you delivered and how it runs
- How the solution meets the need, with headline acceptance-test results
- The main limitations of the solution]

::: toc
:::

[To refresh the Table of Contents after you add or rename a heading, select it and
choose Update Table or Update Field.]

# II. Team Member Roles

[Draft this section in M1 (TP1), and update it at every milestone.]

[List each team member and the specific contributions of that member at each milestone
(TM02). Every member makes a substantive technical contribution at every milestone. If a
member has no entry for a milestone, explain in one line why, and state what that member
did instead. Do not write "N/A" without an explanation.]

[Suggested roles are Project Manager, Systems Analyst, Controls Lead, Test Engineer, and
Communications Lead. Every member contributes to the technical work, whatever their
role.]

: Table 1. Team member contributions

| Milestone | Team members | Specific contributions of each member |
|--------------------------|--------------------|------------------------------------------|
| Problem Scoping (M1) | | |
| Idea Generation (M2) | | |
| Testing and Iteration (M3) | | |
| Solution Development (M4) | | |
| Final Report and Presentation (M5) | | |

[In M1, name an owner for each of the four actuators. The owner is responsible for the
control logic, the parameter-table rows, and the tuning cycles of that actuator in M3
and M4. The team shares responsibility for the integrated behavior and for the CO2
sensor-trust rule.]

[If an owner stops contributing, reassign the actuator as your Code of Cooperation
specifies. Record the change and its date in Table 2.]

: Table 2. Actuator owners

| Actuator | Owner | Changes of owner, with dates |
|--------------------|--------------------|------------------------------------------|
| Heater | | |
| LEDs | | |
| CO2 valve | | |
| Irrigation pump | | |

# III. Problem Scoping

[Draft this section in M1 (TP1). Revise it in M2 and M3 as your evidence requires.]

[Problem scoping happens early in a design process and is revisited throughout it. In
problem scoping, engineers explore the context of the problem, gather information, and
clarify the design requirements. To do this, they engage with the client and the users.]

## a. Problem Statement

[Describe the problem or need. A good problem statement names the client or target users
(PS01), states the need (PS01), and explains why the need matters (PS02).]

[Your client is Mission Control. Use your Client Needs Analysis worksheet and the
in-class client-needs discussion as evidence for this section.]

## b. Design Criteria and Constraints

[List your design requirements as measurable criteria and constraints (PS03). Criteria
describe what success looks like, and constraints describe what limits your solution.
The constraints in this project include the actuator limits, the one-way CO2 valve, the
absence of cooling and dehumidification, solar power, the launch-mass ceiling, the K30
sensor fault, and determinism.]

[Write your criteria before you see the acceptance test. In M4, you compare your
criteria with the acceptance test.]

[Revisit this section in M2 and M3. Simulation evidence may show that a requirement
cannot be met as written. If it does, revise the requirement and record the evidence for
the change (PS05).]

: Table 3. Design requirements

| Criterion or constraint | Metric (how you measure it) | Target and units |
|------------------------------|------------------------------------------|--------------------|
| | | |
| | | |
| | | |

### Trade-off Considerations

[Some criteria compete with each other, so improving one makes another worse. Identify
at least one competing pair of criteria (PS04). For example, tighter temperature control
competes with lower heater energy use.]

## c. Direct Users and Stakeholders

[Identify the users and stakeholders of your design (PS01). They include the Mars crew,
the Mission Control engineers, the maintainers on the next mission, and the crop itself.
Include an image of each user segment, and describe how you empathized with each one.]

: Table 4. Users and stakeholders

| User or stakeholder (image and label) | How you empathized with this user or stakeholder |
|------------------------------------------|------------------------------------------|
| | |
| | |
| | |

## d. Problem Finding

[Determine what went wrong with GHU-1, and support each finding with evidence (SQ01,
PS05). Report your M2 failure investigation of the GHU-1 telemetry log here, and cite
the data behind each claim (IL03). Update this subsection in M2, after you complete the
analysis.]

## e. Background Information

[Research agriculture on Mars, greenhouses, and control systems, and summarize what your
team needs to know to scope the problem (IL01). Cite every source with an APA in-text
citation (IL04), and list it in Section X, References.]

[Record in Table 5 each question your team needed to answer and what you found.]

: Table 5. Background questions and answers

| Question your team needed to answer | What you found, with an in-text citation |
|------------------------------------------|------------------------------------------|
| | |
| | |
| | |

## f. Assumptions about the Problem

[When information is missing, engineers make assumptions to scope the problem. List the
assumptions you made about the need, the users, the environment, and the hardware
(EB02). In M4, you revisit each assumption with your test evidence in Section VIII.]

# IV. Idea Generation

[Draft this section in M2 (TP2). In M3, narrow it to your finalists.]

[Generate a wide range of candidate ideas for the greenhouse system design and its
control approach, including ideas that are not readily obvious (IF01). Use at least four
of the idea generation strategies in this section (IF02). Make each idea easy to
understand, with labeled visuals that show form and function (PC04).]

## a. Functional Decomposition

[Functional decomposition translates the design requirements into functions and
sub-functions. Generating ideas for each sub-function separately produces more
alternatives than brainstorming the whole system at once.]

[Break the job of the greenhouse into sub-functions, such as sensing temperature,
holding a setpoint, preventing CO2 toxicity, and surviving a dust storm. Then generate
ideas for each sub-function (IF02). The ideas for the control sub-functions become your
candidate control strategies.]

: Table 6. Functional decomposition

| Main function | Sub-function | Design ideas for this sub-function |
|--------------------|--------------------|------------------------------------------|
| | | |
| | | |
| | | |

## b. Exploring Prior Art

[Prior art is what others have already built to solve the same problem or a similar one.
Research how controlled-environment greenhouses and their control systems solve these
problems. For each example in Table 7, give an image, a description, its strengths and
weaknesses, and an improved alternative (IF02). Cite every example and every image
(IL04).]

: Table 7. Prior art

| # | Prior art (image, name, and description) | Strengths | Weaknesses | Improved alternative |
|-----|------------------------------|--------------------|--------------------|--------------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## c. Sketching: Greenhouse System Drawing

[Sketching is one of the most common ways to generate and communicate design ideas. Draw
your greenhouse system. Show where each sensor is located, what each actuator does, and
how the control loop connects them. Include the glazing, heater, and battery your team
selected.]

[This drawing is the system drawing deliverable for M2 (IF02, PC04). Insert it as Figure
1, with a caption and alternative text.]

## d. Rapid Prototyping (control-logic mock-ups)

[A low-fidelity prototype is a quick, inexpensive model that checks one function of an
idea. In this project, the low-fidelity prototypes are control-logic mock-ups, such as
rule tables or pseudocode, that you can evaluate before you write code (IF02). Use the
hand-operated sandbox to try them.]

: Table 8. Control-logic mock-ups

| # | Mock-up (rule table or pseudocode) | Idea name | Brief description |
|-----|------------------------------------------|--------------------|------------------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## e. Biomimicry (optional strategy)

[Biomimicry, also called bio-inspired design, generates ideas from the natural world.
The designer asks how plants or animals perform the same function, such as regulating
temperature, water, or gas exchange (IF02). This strategy is optional.]

: Table 9. Ideas from biomimicry

| # | Natural system (image and name) | Idea name | Brief description |
|-----|------------------------------------------|--------------------|------------------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## f. Artificial Intelligence

[Generative AI can suggest ideas outside the experience of your team (IF02). AI output
can be wrong, so plan how you will verify each idea. For each idea, record the prompt
you used, the idea, and your verification plan. Record each use of AI in the AI Use Log
in Section XI, Appendices.]

: Table 10. Ideas generated with [AI platform and model]

| # | Prompt used | Design idea | Plan to verify the idea |
|-----|------------------------------|------------------------------|------------------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |

# V. Thought Experiments

[Draft this section in M2 (TP2).]

[A thought experiment evaluates an idea through discussion, before any testing. Select
about six of your candidate ideas. For each one, discuss its pros and cons against your
criteria and constraints (EB06).]

[Involve every team member in the discussion. The results narrow your ideas to the
finalists you test in M3.]

: Table 11. Thought experiments

| # | Candidate (name and sketch) | Pros | Cons |
|-----|------------------------------------------|------------------------------|------------------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |

# VI. Iteration #1

[Draft this section in M3 (TP3).]

[Describe the first working draft of your controller and the control strategy you chose.
Insert the flowchart of its logic as Figure 2, with a caption and alternative text.
Report the result of your first simulation runs, including whether the crop survived.]

[Summarize the feedback and test evidence that changed your design. Reflect on whether
your understanding of the problem changed (PA02, PA03).]

: Table 12. Changes in Iteration #1

| # | Based on (feedback, data, or test result) | What you changed, and how | Expected result | Observed result |
|-----|------------------------------|------------------------------|--------------------|--------------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

# VII. Prototyping, Testing and Weighted Decision Matrix

[Draft subsections a, b, and d in M3 (TP3). In M4 (TP4), complete subsection c and add
the measured results to subsection d.]

## a. Testing Protocol

[A testing protocol states how you measure success against each criterion (EB01). In
this project, all testing happens in the simulation. For each criterion, name the metric
you read, such as mean temperature error, percent of time with CO2 in band, or sols
survived.]

[State which seeds you run, and confirm that the dust storm and the K30 sensor fault
occur during each run.]

: Table 13. Testing protocol

| Criterion | Metric | Plan to collect evidence (seeds and conditions) |
|------------------------------|------------------------------|------------------------------------------|
| | | |
| | | |
| | | |

## b. Prototypes (candidate designs)

[Present your candidate designs as testable prototypes (IF03). For each prototype, give
the hardware selection and its estimated launch mass, the control strategy for each
actuator, how it handles the K30 sensor fault, and its expected behavior. Run each
prototype in the simulation, on the hardware it assumes.]

: Table 14. Candidate designs

| Candidate | Hardware selection and estimated launch mass | Control strategy for each actuator | K30 fault handling | Expected behavior |
|--------------------|------------------------------|------------------------------|--------------------|--------------------|
| | | | | |
| | | | | |
| | | | | |

## c. Test Results for the Chosen Design

[Present the simulation results for the design you built in tables and charts, with
clear reference to the data (EB03, DV01, DV03). Compare the measured metrics with the
predictions of your M3 decision matrix, and state where each prediction held and where
the data differed.]

[If your team also ran a quick implementation of the runner-up, compare the two designs
here.]

## d. Weighted Decision Matrix (WDM)

[A weighted decision matrix compares design alternatives against criteria that compete
with each other. Each criterion receives a weight that reflects its importance.]

[Carry your M3 decision matrix forward, with the criteria, the weights, a one-line
justification for each weight, and the predicted scores on which you chose your design
(EB04, PC05). In M4, add a column with the measured results of the chosen design, so
that the predictions and the evidence appear side by side (SQ02).]

[Submit the WDM as a spreadsheet that uses cell references and built-in functions
(DV01). Add one predicted-score column for each candidate you compared.]

: Table 15. Weighted decision matrix

| Criterion | Weight and justification | Predicted score, candidate A | Predicted score, candidate B | Measured result, chosen design (M4) |
|--------------------|------------------------------|--------------------|--------------------|--------------------|
| | | | | |
| | | | | |
| | | | | |

# VIII. Iteration #2

[Draft this section in M4 (TP4).]

[In Iteration #2, you optimize the controller. Once the crop survives, tune the
controller to use resources efficiently and to handle the dust storm and the sensor
fault. Record each tune-test cycle in Table 16, and cite the plot or metric behind each
change (PA02, EB05). Include the changes you made in response to the peer review from
another team.]

: Table 16. Changes in Iteration #2

| # | Based on (feedback, data, or test result) | What you changed, and how | Expected result | Observed result |
|-----|------------------------------|------------------------------|--------------------|--------------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

[Revisit each assumption from Section III.f with your test evidence. Mark each one
confirmed, revised, or refuted (EB02).]

: Table 17. Assumptions revisited

| Assumption from Section III.f | Status (confirmed, revised, or refuted) | Evidence |
|------------------------------------------|--------------------|------------------------------------------|
| | | |
| | | |
| | | |

# IX. Overview of Final Design

[Draft subsections a and b in M4 (TP4). Complete subsections c, d, and e in M5 (TP5).]

## a. Detailed Design

\[Describe your final design in enough detail that another engineer could understand and
modify it (PC04, SQ04). Include each of the following items.

- The hardware selection, with a launch-mass breakdown for the glazing, the heater, and
  a battery sized from the worst-sol energy in the acceptance test
- The final flowchart, which matches the code you submit
- The parameter table, with a one-line rationale based on evidence for every value, such
  as "the telemetry log showed X, so we set Y"
- How the controller handles the sensor fault]

: Table 18. Launch-mass breakdown

| Component | Selection | Mass (kg) | Rationale |
|--------------------|------------------------------|--------------------|------------------------------------------|
| Glazing | | | |
| Heater | | | |
| Battery | | | |
| Total | | | |

: Table 19. Controller parameters

| Parameter | Value and units | Rationale based on evidence |
|------------------------------|--------------------|------------------------------------------|
| | | |
| | | |
| | | |

## b. Data on the Final Solution

[Show that your controller meets the requirements (EB01). Present your final
acceptance-test results and the performance plots from your analysis script (EB03, DV01,
DV03). Include temperature tracking through the dust storm, CO2 through the sensor
freeze, and actuator effort. Format each plot professionally, with a numbered caption.]

## c. Novel Aspects of the Solution

[Describe what is new or unusual about your design (SQ04).]

## d. Trade-off Decisions and Limitations

[All design involves trade-offs. State the trade-off decisions your team made (SQ03). A
solution built in a few weeks has limitations, so describe the limitations of yours
(SQ03, EC02).]

[Report the disposition of every requirement your team revised (PS05). For each one,
state what the client asked for, what this hardware can achieve, what hardware change
would meet the original target, and what your controller delivers.]

: Table 20. Revised requirements

| Requirement | Client target | Achievable with this hardware | Hardware change that meets the original target | Delivered by your controller |
|--------------------|--------------------|--------------------|------------------------------|--------------------|
| | | | | |
| | | | | |

[Add a responsible-use note. The greenhouse shares an airlock with the crew. State how
your design protects the crew and where the design should not be trusted (EC01-EC03).]

[Examine the hardware one actuator at a time. For each actuator, compare the worst case
your controller must cover with what the device can deliver, and state whether the limit
you reached was your control logic or the hardware. Where the hardware is the limit,
report the gap and the recommendation you would make to the client, with its cost (SQ03,
EB05).]

: Table 21. Actuator limits

| Actuator | Worst-case demand | Device capability | Limit reached (control logic or hardware) | Effect on the crop, recommendation, and cost |
|--------------------|--------------------|--------------------|--------------------|------------------------------|
| Heater | | | | |
| LEDs | | | | |
| CO2 valve | | | | |
| Irrigation pump | | | | |

## e. Lessons Learned

[Reflect on the problem-solving and design process of your team (PA01-PA03). Describe
its strengths, what you would change, and how your thinking developed. Write about
process and skills here, not about changes to the design.]

# X. References

[Compile this section across the project, and finalize it in M5 (TP5).]

[List every source in APA format (IL05). Cite every external source and every image of
prior art. The
[Purdue OWL APA guide](https://owl.purdue.edu/owl/research_and_citation/apa_style/apa_style_introduction.html)
covers in-text citations and reference lists.]

# XI. Appendices

[Put any optional supporting material first. The AI Use Log comes last, as the AI-use
ground rules of the project require.]

## AI Use Log

[Add one record to the log for each conversation with an AI tool that contributed to
your work. A new conversation starts a new record. Number the records in order, and give
each one a level 3 heading, as in the example below.]

\[Each record begins with these items:

- **Team member and date:** who used the tool, and when.
- **Tool:** the product name, and the account you signed in with.
- **Purpose:** what you asked the tool to do, and which ground rule permits it.
- **What we used:** the information from the responses that entered your work, and
  where it appears in the report or code.
- **What we rejected:** any suggestion you did not use, and why.
- **How we verified it:** the test, calculation, or source that confirmed what you used.

The transcript follows the items.]

[Label every request in the transcript with the model and the effort setting it ran on.
The model is the name the tool gives the model, with its version number. The effort
setting is the reasoning level selected for that request, such as a quick mode or a
deeper thinking mode. Copy both exactly as the tool displays them. Some tools hide the
model name. For those tools, write "Model not shown" and record the mode name that the
tool does display. Label each request separately, because a setting can change in the
middle of a conversation.]

[Paste the complete conversation as text: every request and every response, in order and
unedited, including responses you did not use. Share links and screenshots do not
replace the text. A link can expire or require a login, and the grading team reads the
full exchange in the PDF.]

[The record below is an example. Delete it, and add your own records in the same
format.]

### AI Record 1: Integral Windup in the Night Heater Loop

- **Team member and date:** Priya Raman, October 27, 2026.
- **Tool:** Microsoft 365 Copilot Chat, signed in with a Purdue account.
- **Purpose:** Critique the integral and clamp handling in the heater logic of our
  flowchart. The ground rules permit critique of flowchart and pseudocode logic.
- **What we used:** Conditional integration, which pauses the integral term while the
  heater command is clamped. It is step 6 of the flowchart in Figure 2, Section VI.
- **What we rejected:** The suggestion to cap the heater at 80 % of its rating. The
  heater is the only heat source at night, and a lower cap removes 400 W from the worst
  night without preventing windup at the new limit.
- **How we verified it:** We ran the same cold night in the sandbox with and without the
  change. Without it, the air temperature overshot the night setpoint of 18 degrees
  Celsius by 2.6 degrees after the heater left saturation. With it, the overshoot was
  0.4 degrees. Table 12 in Section VI records both runs.

**Request 1.** Model: GPT-5. Effort: Quick response.

Our greenhouse controller runs a PI loop on air temperature. The heater command is
clamped to 0 to 100 % of 2000 W. On cold nights the heater stays at 100 % for hours.
Each tick, we compute the error as the setpoint minus the temperature, add the error
times the tick length to the integral, and set the heater command to Kp times the error
plus Ki times the integral, clamped to 0 to 100 %. What problems do you see with the
integral term?

**Response 1.**

The integral term winds up. While the heater is clamped at 100 %, the error stays
positive, so the integral keeps growing even though the heater cannot deliver more heat.
When the air finally warms past the setpoint, the large integral holds the heater on,
and the temperature overshoots until the integral unwinds.

Two common fixes exist. Conditional integration pauses the integral update while the
output is clamped. Back-calculation drives the integral toward the value that matches
the clamped output. You could also cap the heater at about 80 % of its rating, so that
it never reaches saturation.

**Request 2.** Model: GPT-5. Effort: Think deeper.

Explain conditional integration step by step for our loop. Which fix is simpler to test
in a simulation?

**Response 2.**

Conditional integration adds one check before the integral update. If the command is at
the upper clamp and the error is positive, skip the update. If the command is at the
lower clamp and the error is negative, skip the update. Otherwise, update the integral
as before. The check stops the integral from growing only in the direction that pushes
the output further into the clamp.

Conditional integration is simpler to test, because it adds no tunable parameter. Run
the same cold night with and without the check, and compare the overshoot after the
heater leaves saturation. Back-calculation adds a tracking gain, which needs its own
tuning before the comparison means anything.
