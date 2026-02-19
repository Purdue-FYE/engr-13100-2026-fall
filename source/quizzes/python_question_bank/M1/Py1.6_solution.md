### Q1.6 Strings and Indexing

Consider the following line of code:

    text = "Python Programming"

(a) What is the result of text.strip()?

    "Python Programming"

(b) What does text.lower() return?

    "python programming"

(c) What character is at index 3 of text.strip()?

    "h"

(d) What substring is returned by text.strip()[7:18]?

    "Programming"

(e) Explain what happens if you try to access text[50].

    This will cause an error because the string is much shorter than 51 characters. Python will raise:

    IndexError: string index out of range