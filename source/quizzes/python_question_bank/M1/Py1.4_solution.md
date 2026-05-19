### Q1.4 == vs is (Conceptual Reasoning)

Two lists, A and B, are created separately, and both contain the same values:

    A = [1, 2, 3]
    B = [1, 2, 3]

Answer the following questions without running any code:

(a) If you compare A and B using `==`, would the result be `True` or `False`? Explain briefly.

    Answer: True

    Explanation:

    The == operator checks whether the contents of the two lists are the same. Since both lists contain the same values in the same order, the comparison evaluates to True.

(b) If you compare A and B using `is`, would the result be `True` or `False`? Explain briefly.

    Answer: False

    Explanation:

    The is operator checks whether both variables refer to the same object in memory. Even though A and B look identical, they were created separately, so they point to two different list objects.

(c) In your own words, describe the conceptual difference between using `==` and using `is` in Python.

    Answer:
    == compares values or contents (i.e., do these objects look the same?).

    is compares identity (i.e., are these two names pointing to the exact same object in memory?).

(d) Give one example of a situation where using `is` is more appropriate than using `==`.

    Answer:
    A common example is checking for None:

    if value is None:
        ...
