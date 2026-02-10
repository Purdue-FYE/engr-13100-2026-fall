## Question a) Is linear regression appropriate for this dataset? Why or why not?
No, the data does not appear to follow a linear trend.

## Question b) Rewrite the regression equation, replacing the generic variables y and x with descriptive variables.
Mean Monthly Temperature = -0.0032 * Elevation + 18.022

## Question c) One of your teammates tells you that the mean monthly temperature around the world is 22 degrees Celsius at sea level (0 m elevation). He suggests fixing the intercept to 22. 

### Question c.1) What will happen to the slope of your trendline if you fix the intercept to 22?
- [ ] It will increase
- [x] It will decrease
- [ ] It will stay the same
- [ ] Not enough information to tell

### Question c.2) What will happen to the least squares regression R-squared value if you fix the intercept to 22?
- [ ] It will increase
- [x] It will decrease
- [ ] It will stay the same
- [ ] Not enough information to tell

### Question c.3) Provide one argument on why it is a good idea to fix the intercept to 22 before performing regression analysis.
If this is a known constant, it might make sense to fix the intercept so the model more-closely follows the theoretical values.

### Question c.4) Provide one argument on why it is a bad idea to fix the intercept to 22 before performing regression analysis.
We collected real data, not theoretical data, so we should use the optimal regression line for that data.
