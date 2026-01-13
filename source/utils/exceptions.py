from os import path
import traceback
import textwrap


inf_loop_hint = "Make sure your program isn't stuck in an infinite loop."
return_hint = "Try using a `return` statement instead."

wrapper = textwrap.TextWrapper(
    initial_indent="  ",
    subsequent_indent="  ",
)


def indent(string, pad="  "):
    return "\n".join([pad + line for line in string.splitlines()])


def format_error_msg(error_msg, hint=None):
    hint = f"\n\nHint:\n{wrapper.fill(hint)}" if hint else ""
    return f"{wrapper.fill(error_msg)}{hint}"


def handle_error(e, error_msg):
    stack_summary = traceback.extract_tb(e.__traceback__)
    short_stack_summary = []
    for frame_summary in stack_summary:
        dirname, filename = path.split(frame_summary.filename)

        # Skip frames from the autograding system. This is usually the
        # first frame, which contains the call to the submitted code in
        # this try block, and the last 1 or 2 frames which typically
        # contain the patched function.
        if "/tests" in dirname or "/usr" in dirname or filename == "<string>":
            continue

        # Remove the path information from the filename in each frame
        # summary.  This makes the error message clearer while also
        # hiding the autograder's directory structure.
        frame_summary.filename = filename

        short_stack_summary.append(frame_summary)

    # Format the traceback with special handling for syntax errors.
    if isinstance(e, SyntaxError):
        # Remove the path information from the filename.
        dirname, filename = path.split(e.filename)
        e.filename = filename

    formatted_traceback = (
        (
            "Traceback (most recent call last):\n"
            + "".join(traceback.format_list(short_stack_summary))
        )
        if short_stack_summary
        else ""
    ) + "".join(traceback.format_exception_only(e))

    return indent(error_msg + "\n\n" + formatted_traceback)

class InputError(Exception):
    """Custom Exception type."""

    def __init__(self, hint=None):
        error_msg = "Encountered call to `input` during import."
        hint = (
            "Avoid calling `input` in the global scope "
            "(i.e. outside of any function or other code block)."
            + hint if hint else ""
        )
        self.msg = format_error_msg(error_msg, hint)

    def __str__(self):
        return self.msg


class EndOfInputError(Exception):
    """Custom Exception to raise when submitted code requests too much input."""

    def __init__(self, hint=None):
        error_msg = "Your program requested user input more times than expected."
        hint = f"{hint}  {inf_loop_hint}" if hint else inf_loop_hint
        self.msg = format_error_msg(error_msg, hint)

    def __str__(self):
        return self.msg


class LogLimitExceededError(Exception):
    """Custom Exception to raise when the log length exceeds some limit."""

    def __init__(self, hint=None):
        error_msg = "Your program produced much more output than was expected."
        hint = f"{hint}  {inf_loop_hint}" if hint else inf_loop_hint
        self.msg = format_error_msg(error_msg, hint)

    def __str__(self):
        return self.msg



class ExcessFunctionCallError(Exception):
    """Custom Exception to raise when submitted code calls a function more
    times than expected.
    """

    def __init__(self, func_name, hint=None):
        error_msg = (
            f"Your program called the `{func_name}` function"
            " more times than expected."
        )
        hint = f"{hint}  {inf_loop_hint}" if hint else inf_loop_hint
        self.msg = format_error_msg(error_msg, hint)

    def __str__(self):
        return self.msg

class ExitError(Exception):
    """Custom Exception to raise when submitted code calls `exit()`."""

    def __init__(self, hint=None):
        error_msg = "Calling the `exit()` function is not allowed in this course."
        hint = f"{hint}  {return_hint}" if hint else return_hint
        self.msg = format_error_msg(error_msg, hint)

    def __str__(self):
        return self.msg


class QuitError(Exception):
    """Custom Exception to raise when submitted code calls `quit()`."""

    def __init__(self, hint=None):
        error_msg = "Calling the `quit()` function is not allowed in this course."
        hint = f"{hint}  {return_hint}" if hint else return_hint
        self.msg = format_error_msg(error_msg, hint)

    def __str__(self):
        return self.msg

