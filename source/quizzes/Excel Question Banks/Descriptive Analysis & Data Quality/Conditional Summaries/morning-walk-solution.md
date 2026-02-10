Your roommate has a 7:30 am chemistry class and doesn't like walking to class in the dark. It takes 20 minutes to walk from the dorm to the class.

They made a spreadsheet in Excel showing the time they left for class, in "minutes after 7:00 am". and the time the sunrise was that day, with the same units. 

![Spreadsheet containing departure times and sunrise times](morning-walk-img.png)

### Question a) Read questions b, c, and d. What might be a helpful calculation to add to column E?

Sample solution: I would calculate the difference between columns C and D (D - C), meaning numbers > 0 indicate they walked partially or completley in the dark, numbers <= 0 indicating that they walked completley in the light.

Sample solution: I would calculate the arrival time to class by adding 20 to each cell in column C, showing that numbers > 30 mean they arrived late to class.

Sample solution: Reasonable answer adequately explained, referring to data that can be used for at least one of the following sub-questions.


What column label would you put in cell E3?

Sample solution: Difference in departure time and sunrise time (minutes)

Sample solution: Arrival time (minutes after 7:00am)

sample solution: Professionally formatted answer consistent with reasobable previous response

What formula would you put in cell E4?

Sample solution: =D4 - C4 (or C4 - D4)

Sample solution: =C4 + 20

How would you populate the column?

I would drag the formula in cell E4 down the column.


### Question b) Your roommate wants to know how many days they walked to class partially or completley in the dark. Write an Excel formula that would calculate this.

Sample solution: =COUNTIF(E4:E24, ">0")

Sample rubric:
- Contains correct formula, COUNTIF
- Contains correct range, E4:E24, with colon notation (or other calculation with other columns in the same rows)
- Contains correct inequality or calculation consistent with table setup in previous questions
- Second argument is in quotation marks, both inputs are inside parentheses, equals sign at start of formula

### Question c) Your roommate wants to know how many days they walked to class completley in the light. Write an Excel formula that would calculate this.

Sample solution: =COUNTIF(E4:E24, "<=0"); or answer consistent with spreadsheet setup

### Question d) Your roommate wants to know how many days they were late to class. Write an Excel formula that would calculate this.

Sample solution: =COUNTIF(C4:C24, "<10"); or answer consistent with spreadsheet setup in column E
