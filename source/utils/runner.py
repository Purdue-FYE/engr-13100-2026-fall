"""Provide a mock user to run sample code."""

import base64
import os
import re
import sys
import textwrap
from contextlib import ExitStack, contextmanager
from copy import deepcopy
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from utils.docs import make_call_str, ordinalize
from utils.exceptions import EndOfInputError, LogLimitExceededError, handle_error
from utils.importer import Importer


@contextmanager
def change_working_dir(destination):
    try:
        cwd = os.getcwd()  # get current directory
        sys.path.insert(0, str(destination.absolute()))
        os.chdir(destination)  # change directory
        yield
    finally:
        os.chdir(cwd)  # change back to original directory
        sys.path.remove(str(destination.absolute()))


class LogIO(StringIO):
    """A string io object with a character limit."""

    def __init__(self, log_limit=0):
        """Initialize with an unlimited default limit (0 characters)."""
        super().__init__()
        self.log_limit = log_limit

    def __len__(self):
        """Return the number of characters in the log."""
        return len(self.getvalue())

    def write(self, s):
        """Wrap inherited `write()` with a length limit check."""
        super().write(s)

        # Check if limit is exceeded after write so the offending string
        # will be in the log for debugging.
        if self.log_limit and len(self) > self.log_limit:
            raise LogLimitExceededError()


class Runner:
    """Manages and log interactions with reference solutions."""

    wrapper = textwrap.TextWrapper(initial_indent="  ", subsequent_indent="  ")

    def __init__(self, module, obj_name="main", patches=None):
        """Initialize a user."""

        self.module = module
        self.obj_name = obj_name
        self.entries = iter("")
        self.log = LogIO()
        self.log_context = 2  # Number of additional lines of context to include.

        # Make a list of stream positions starting from the beginning and
        # adding one at each user entry.
        self.interactions = [self.log.tell()]

        # Determine if module is a Python or MATLAB file.
        # Generate a list of all files matching the module name.
        files = list(Path(module).parent.glob(f"{Path(module).stem}.*"))
        assert len(files) == 1, (
            f"Expected exactly one file matching {module}. Found: {files}"
        )
        if files:
            self.tmp_dir = Path(module).parent
            if files[0].suffix == ".py":
                self.Python = True
                self.MATLAB = False

            elif files[0].suffix == ".m":
                self.Python = False
                self.MATLAB = True

        if self.MATLAB:
            self.obj_name = "solution"

        self.returned_values = None

        self.patches = [
            {"args": ["sys.stdout", self.log]},
            {"args": ["builtins.input", self.responder]},
            {
                "args": [
                    "builtins.exit",
                    lambda *args, **kwargs: exec("raise ExitError"),
                ],
            },
            {
                "args": [
                    "builtins.quit",
                    lambda *args, **kwargs: exec("raise QuitError"),
                ],
            },
        ]
        if patches:
            self.patches.extend(patches)

    def format_log(self, interaction=0, n_lines=None):
        lines = self.read_log_lines(interaction, n_lines=n_lines)
        if lines:
            string = (
                "\n\nline |Input/Output Log:\n"
                + f"{70 * '-'}\n"
                + "".join([f"{n + 1:4d} |{line}" for n, line in enumerate(lines)])
            )
        else:
            string = ""
        return string

    def get_value(self, interaction=0, line_n=1, value_n=1):
        """Return the value_n th float in line `line_n`, indexed from the
        prompt for user interaction `interaction`.
        """

        values = self.get_values(interaction=interaction, line_n=line_n)

        try:
            msg = False
            value = values[value_n - 1]
        except IndexError:
            value_nth = ordinalize(value_n)
            line_nth = ordinalize(line_n)
            msg = (
                "\n"
                + self.wrapper.fill(
                    f"Looking for the {value_nth} value "
                    + f"in the {line_nth} output line, "
                    + f"but only found {len(values)} value(s) "
                    + f"in line {line_n}."
                )
                + self.format_log(interaction, line_n + self.log_context)
            )

        if msg:
            # TODO to something with the error message
            pass

        return value

    def get_values(self, interaction=0, line_n=1):
        """Return all the values matching a number like pattern in line
        `line_n`, indexed from the prompt for user interaction `interaction`.
        """
        pattern = r"""(?x:                 # Start a verbose pattern
                      -?                   # 0 or 1 leading minus signs
                      [0-9]{1,3}           # 1 to 3 digits
                      (?:                  # Start a non-capturing group
                        (?:                #   Start a non-capturing group
                          ,[0-9]{3}        #     literal comma 3 digits
                        )+                 #     1 or more times
                        |                  #   OR
                        (?:[0-9]*)         #   Any number of digits
                      )                    #
                      (?:                  # Start a non-capturing group
                        \.                 #   A literal period
                        [0-9]*             #   0 or more digits
                      )?                   # 0 or 1 times
                      (?:                  # Start a non-capturing group
                        e[+-]              #   literal e followed by + or -
                        [0-9]+             #   1 or more digits
                      )?                   # 0 or 1 times
                  )"""

        line_string = self.read_log_line(interaction, line_n)
        match_strings = re.findall(pattern, line_string)
        value_strings = [match.replace(",", "") for match in match_strings]

        try:
            msg = False
            values = [float(value_str) for value_str in value_strings]
        except ValueError as e:  # Just in case the pattern matching fails.
            msg = (
                "Test failed due to an error. "
                + f'The error was "{e.__class__.__name__}: {e}". '
                + "This is a bug in the autograder. "
                + "Please notify your instructor."
            )
        if msg:
            # TODO to something with the error message
            pass

        return values

    def read_log(self, interaction=0, start=0, n_lines=None):
        """Return a string of up to `n_lines` lines of IO starting from the
        prompt for user interaction `interaction`.
        """
        return "".join(self.read_log_lines(interaction, start, n_lines))

    def read_log_line(self, interaction=0, line_n=1):
        """Return line number `line_n` of IO as a string, indexed from the
        prompt for user interaction `interaction`.
        """
        lines = self.read_log_lines(interaction)
        try:
            msg = False
            line_string = lines[line_n - 1]
        except IndexError:
            msg = (
                "\n"
                + self.wrapper.fill(
                    f"Looking for line {line_n}, "
                    + f"but output only has {len(lines)} lines."
                )
                + self.format_log(interaction, line_n)
            )
        if msg:
            # TODO to something with the error message
            pass

        return line_string

    def read_log_lines(self, interaction=0, start=0, n_lines=None):
        """Return a list of up to `n_lines` lines of IO starting from the
        prompt for user interaction `interaction`.
        """
        self.log.seek(self.interactions[interaction])
        start = start and start - 1 or 0
        stop = n_lines and start + n_lines or n_lines
        return self.log.readlines()[start:stop]

    def responder(self, string=""):
        """Override for builtin input to provide simulated user responses."""

        # Save the IO stream location
        self.interactions.append(self.log.tell())

        # Log prompt
        self.log.write(string)

        # Get the user's next entry
        try:
            entry = str(next(self.entries))
        except StopIteration as e:
            # Chain StopIteration to custom EndOfInputError which can be
            # handled later.
            raise EndOfInputError from e

        # Log entry
        self.log.write(f"<user-input>{entry}</user-input>\n")

        return entry

    def call_obj(
        self,
        entries="",
        args=(),
        kwargs={},
        log_limit=0,
        debug=False,
        suppress_output=False,
    ):
        """Have a simulated user call the object."""

        if entries:
            # Flatten entries to a list.
            flat_entries = []
            for entry in entries:
                if isinstance(entry, list):
                    flat_entries.extend(entry)
                else:
                    flat_entries.append(entry)
            self.entries = iter(flat_entries)

        if log_limit:
            self.log.log_limit = log_limit

        msg = False
        call_str = make_call_str(self.obj_name, args, kwargs)
        if self.MATLAB and suppress_output:
            call_str += ";"
        error_msg = "\n" + self.wrapper.fill(
            f"Your `{self.obj_name}` malfunctioned"
            + f" when called as `{call_str}`"
            + ((entries) and f" with entries {entries}." or ".")
        )
        try:
            if self.MATLAB:
                print("Starting MATLAB process.")
            with ExitStack() as stack:
                # Apply each patch.
                for p in self.patches:
                    stack.enter_context(
                        patch(
                            *p.get("args", ()),  # permit missing args
                            **p.get("kwargs", {}),  # permit missing kwargs
                        )
                    )

                stack.enter_context(change_working_dir(self.tmp_dir))

                if self.Python:
                    # Import the test modules obj_name object.
                    module = self.module.replace("source/", "").replace("/", ".")
                    obj = Importer.import_obj(module, self.obj_name)

                    # Call the attached object with copies of r args and kwargs.
                    self.returned_values = obj(*deepcopy(args), **deepcopy(kwargs))
                elif self.MATLAB:
                    # Run init_entries and reference solution from temporary directory.
                    import requests

                    url = "http://localhost:8000/run"
                    file_paths = set(
                        f
                        for f in Path().glob("**/*")
                        if f.is_file() and f.suffix not in [".pyc"]
                    )
                    files = [
                        ("files", open(file_path, "rb")) for file_path in file_paths
                    ]
                    entries = ", ".join(
                        "'" + str(entry) + "'" for entry in self.entries
                    )
                    args = ", ".join(str(arg) for arg in args)
                    response = requests.post(
                        url,
                        files=files,
                        data={
                            "call_str": call_str,
                            "entries": entries,
                            "args": args,
                        },
                    )
                    self.log.write(response.json().get("output"))

                    # Recover new files created by the MATLAB process.
                    new_files = response.json().get("new_files", [])
                    for file in new_files:
                        with open(file["path"], "wb") as f:
                            f.write(base64.b64decode(file["content_base64"]))

            if self.MATLAB:
                print("MATLAB process complete.")

        except Exception as e:
            msg = handle_error(e, error_msg)
        else:
            try:  # Check for left over entries.
                next(self.entries)
            except StopIteration:
                pass  # The expected result.
            else:
                msg = (
                    error_msg
                    + "\n\nHint:\n"
                    + self.wrapper.fill(
                        "Your program ended before the user finished entering input."
                    )
                )

        if msg:
            raise Exception(msg)

        if debug:
            print(self.log.getvalue())

        return self.returned_values
