### Question a) Write your formula in cell F4.
=IF(F3 + $C$1 >= 60, F3 + $C$1 - 60, F3 + $C$1)
or
=IF(F3 + $C$1 > 59, F3 + $C$1 - 60, F3 + $C$1)
or equivalent

### Question b) How would you populate the rest of column F?
I would copy/drag the formula in cell F4 down the column.

### Question c) Another athlete is sharing the lane, and starts every interval 5 seconds after the first athlete. Add a column to Table 2 to show what clock time they start their laps at.
|Second athlete leaves when the clock says|
|---|
|=IF(F3 + 5 >= 60, F3 + 5 - 60, F3 + 5)|

Copy/drag the formula in cell G3 down the column
