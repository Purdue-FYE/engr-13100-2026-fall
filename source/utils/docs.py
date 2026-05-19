"""Functions to generate customized docstrings for parameterized tests."""


def calc_log_limit(expected_log):
    """Calculate a log character limit as some minimum number of
    characters plus a multiple of the length of the expected log.
    """
    return int(200 + 1.5 * len(expected_log))


def ordinalize(n):
    """Return the ordinal number representation of n."""

    # Set the most common suffix
    suffix = "th"

    # Handle special cases:
    # i.e. numbers ending in 1, 2 or 3 but not ending in 11, 12, or 13
    ones, tens = abs(n) % 10, abs(n) % 100
    if ones in (1, 2, 3) and tens not in (11, 12, 13):
        suffix = ("st", "nd", "rd")[ones - 1]

    return f"{n}{suffix}"


def make_call_str(func_name="main", args=[], kwargs={}):
    """Construct and return a function call string from its name, and
    arguments.
    """
    # Create a list of position argument strings.
    args_lst = list(map(repr, args))

    # Add keyword argument strings.
    args_lst.extend(f"{k}={repr(v)}" for k, v in kwargs.items())

    # Construct the function call with a comma separated list of arguments.
    call_str = f"{func_name}({', '.join(args_lst)})"

    return call_str


def make_line_range(start, n_lines):
    """Return the range of lines being checked expressed in words."""
    if n_lines == 1:
        return f"line {start}"
    else:
        stop = n_lines and start + n_lines - 1 or "the end"
        return f"lines {start} through {stop}"


def oxford_list(sequence):
    """Return the strings in sequence formatted as an Oxford list."""
    if len(sequence) <= 2:
        # Handle sequences of 0, 1, or 2 items.
        return " and ".join(sequence)
    else:
        # Handle sequences of 3 or more items.
        last = sequence[-1]
        not_last = ", ".join(sequence[:-1])
        return f"{not_last}, and {last}"


def func_return_doc(func, num, param):
    """Return parameterized docstring when checking value(s) returned from a
    function call.

    Deprecated: use function_return() instead.
    """

    def fill_param(name="", args=[], kwargs={}, entries=()):
        """Return parameters, filling in with defaults where necessary."""
        return name, args, kwargs, entries

    name, args, kwargs, entries = fill_param(*param.args, **param.kwargs)
    call_str = make_call_str(name, args, kwargs)
    docstring = f"Check value(s) returned from function call `{call_str}`" + (
        entries and f" with entries={entries}." or "."
    )

    return docstring


def main_output_doc(func, num, param):
    """Return a custom docstring for parameterized tests."""

    def fill_param(label="", entries=[]):
        """Return parameters, filling in with defaults where necessary."""
        return label, entries

    _, entries = fill_param(*param.args)

    call_str = make_call_str()
    docstring = (
        f"Check number of lines of output from `{call_str}` with entries={entries}."
    )

    return docstring


def main_results_doc(func, num, param):
    """Return parameterized docstring when checking value(s) in the text output
    of the main function.
    """

    def fill_param(label="", line_n=1, value_n=1, entries=[]):
        """Return parameters, filling in with defaults where necessary."""
        return label, line_n, value_n, entries

    _, line_n, value_n, entries = fill_param(*param.args, **param.kwargs)
    call_str = make_call_str()
    docstring = (
        f"Check {ordinalize(value_n)} value "
        f"on output line {line_n} "
        f"from `{call_str}` with entries={entries}."
    )

    return docstring


def main_formatting_doc(func, num, param):
    """Return parameterized docstring when checking formatting of the lines
    output by the main function.

    Deprecated: use output_line_formatting() instead.
    """

    def fill_param(label="", line_n=1, entries=[]):
        """Return parameters, filling in with defaults where necessary."""
        return line_n, entries

    line_n, entries = fill_param(*param.args)
    call_str = make_call_str()
    docstring = f"Check the formatting of output line {line_n} from `{call_str}`" + (
        entries and f" with entries={entries}." or "."
    )

    return docstring


def output_line_matches_reference(func, num, param):
    """Return parameterized docstring when checking formatting of output lines."""

    def fill_param(func_name, entries=[], line_n=1, hint="", patches=""):
        """Return parameters, filling in with defaults where necessary."""
        return line_n, entries

    line_n, entries = fill_param(*param.args, **param.kwargs)
    call_str = make_call_str()
    docstring = (
        f"Check that the formatting of output line {line_n} from `{call_str}` "
        + (entries and f"with entries={entries} " or "")
        + "matches the reference line."
    )

    return docstring


def output_line_matches_pattern(func, num, param):
    """Return parameterized docstring when checking formatting of output lines."""

    def fill_param(func_name, entries=[], line_n=1, pattern="", hint=""):
        """Return parameters, filling in with defaults where necessary."""
        return line_n, entries, pattern

    line_n, entries, pattern = fill_param(*param.args, **param.kwargs)
    call_str = make_call_str()
    docstring = (
        f"Check that the formatting of output line {line_n} from `{call_str}` "
        + (entries and f"with entries={entries} " or "")
        + f"matches the pattern '{pattern}'."
    )

    return docstring


def turtle_path_doc(func, num, param):
    """Return parameterized docstring when checking a turtle path."""

    def fill_param(
        region_a="",
        region_b="",
        mode="",
        threshold=None,
        hint="",
        image_a="",
        image_b="",
    ):
        """Return parameters, filling in with defaults where necessary."""
        return region_a, region_b, mode, threshold

    region_a, region_b, mode, threshold = fill_param(*param.args, **param.kwargs)

    docstring = (
        f"Check that the {region_a} has {mode} {threshold} pixels in the {region_b}."
    )

    return docstring


def turtle_path_doc_2(func, num, param):
    """Return parameterized docstring when checking a turtle path."""

    region_a, region_b, mode, threshold, _, _, _, _ = param.args

    docstring = (
        f"Check that the {region_a} has {mode} {threshold} pixels in the {region_b}."
    )

    return docstring


def turtle_letter_draws(func, num, param):
    """Return parameterized docstring when checking value(s) returned from a
    function call.
    """

    def fill_param(func_name="", args=[], kwargs={}, entries=(), hint="", patches=""):
        """Return parameters, filling in with defaults where necessary."""
        return func_name, args, kwargs, entries

    func_name, args, kwargs, entries = fill_param(*param.args, **param.kwargs)
    call_str = make_call_str(func_name, args, kwargs)
    docstring = f"Check value(s) returned from function call `{call_str}`" + (
        entries and f" with entries={entries}." or "."
    )

    return docstring
