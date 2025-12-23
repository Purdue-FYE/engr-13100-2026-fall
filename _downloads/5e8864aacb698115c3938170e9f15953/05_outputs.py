"""
OUTPUTS in Python
- print()
- format()

print() function - prints the given object to the standard output device (screen)
      world = 616
    - print("Hello World")
    - print("Hello", "World")
    - print("Hello", "World", world)
    - print("Hello", "World", 616, sep="***", end="!")
    - print("There are",120,"students in the class", sep=" ", end=".\n")

format() function - accepts a number and a format specifier and returns as a string
    Syntax: format(number, format_specifier)

    format_specifier syntax - "[width][grouping_option][.precision][type]"
        - width - minimum number of characters to be printed (default is 0)
        - grouping_option - comma (,) to use comma as a thousand separator
        - precision - number of decimal places to be printed
        - type - d for integer, f for float, s for string

    Examples:
        format(123.4567, ".2f")       # Output is "123.46"
        format(1234.56789, "10,.2f")  # Output is "  1,234.57"
        format(1234, "10_d")          # Output is "     1_234"
        format(0.2, "0.0%")           # Output is "20.0%"
        format(12345.6789, "e")       # Output is "1.234568e+04" which is 1.234568 x 10^4
        format(12345.6789, "E")       # Output is "1.234568E+04" which is 1.234568 x 10^4
        format(12345.6789, ".2e")     # Output is "1.23e+04" which is 1.23 x 10^4
        format(0.00000012345, ".4E")  # Output is "1.2345E-07" which is 1.2345 x 10^-7

f-string - introduced in Python 3.6
    Syntax: f"string {variable}"
    Example:
        item = "apple"
        cost = 1234.56789
        f"{item} costs ${cost}"             # Output is "apple costs $1234.56789"
        print(f"{item} costs ${cost:,.2f}") # Output is "apple costs $1,234.57"
"""
