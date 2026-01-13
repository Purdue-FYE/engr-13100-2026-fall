from textwrap import TextWrapper

from PIL import Image


def markdown_table(fields, rows, alignments=None):
    """Format a table for use in Markdown.

    Some care is taken to ensure the column are aligned.

    E.g.

    | field 1        | field 2        |
    |:--------------:|:--------------:|
    | row 1, field 1 | row 1, field 2 |
    | row 2, field 1 | row 2, field 2 |

    """
    # Pad each row to the same length.
    max_len = max(len(row) for row in rows)
    for row in rows:
        row.extend([""] * (max_len - len(row)))

    # Pad alignments to the same length.
    if alignments is None:
        alignments = []
    alignments.extend(["center"] * (max_len - len(alignments)))

    # Calculate the minimum width of each column.
    widths = [max(len(str(item)) for item in col) for col in zip(fields, *rows)]

    header_row = (
        "| "
        + " | ".join(f"{field:^{width}}" for field, width in zip(fields, widths))
        + " |\n"
    )
    alignment_row = "|"
    for width, alignment in zip(widths, alignments):
        if alignment == "left":
            alignment_row += ":" + "-" * width + " |"
        elif alignment == "right":
            alignment_row += " " + "-" * width + ":|"
        else:
            alignment_row += ":" + "-" * width + ":|"
    alignment_row += "\n"
    body_rows = "\n".join(
        [
            "| "
            + " | ".join(f"{str(field):{width}}" for field, width in zip(row, widths))
            + " |"
            for row in rows
        ]
    )

    return header_row + alignment_row + body_rows


def format_test_case_table(cases, labels, table_name):
    fields = ["Case"] + labels
    rows = [
        [name] + case.get("entries", []) + case.get("args", [])
        for name, case in cases.items()
    ]

    wrapper = TextWrapper(break_long_words=False)
    return (
        wrapper.fill(
            f"Use the values in {{numref}}`tab:{table_name}` below to test your"
            " program."
        )
        + "\n"
        "\n"
        "```{table} Test Cases\n"
        f":name: tab:{table_name}\n"
        ":class: test-case-table\n"
        "\n" + markdown_table(fields, rows) + "\n"
        "```\n"
        "\n"
        + wrapper.fill(
            "Ensure your program's output matches the provided samples exactly."
            " This includes all characters, white space, and punctuation. In"
            " the samples, user input is <span class=user-input>highlighted"
            " like this</span> for clarity, but your program should not"
            " highlight user input in this way."
        )
        + "\n"
    )


def format_io_log(log, name=None, title=None, args=None, suppress_output=False):
    # Try to construct the call string.  We should probably do this in User, where the
    # script is actually called, and then include it in the log.
    identifier = "teamnumber" if "team" in title else "username"
    filename = f"{title}{identifier}"
    if title.startswith("py") or title.startswith("tp"):
        call_string = f"$ <user-input>python3 {filename}.py</user-input>\n"
    elif title.startswith("ma"):
        if args:
            filename += "(" + ", ".join(map(str, args)) + ")"
        if suppress_output:
            filename += ";"
        call_string = f">> <user-input>{filename}</user-input>\n"
    else:
        call_string = "\n"
    return (
        "\n"
        f"```{{admonition}}{f' Case {name}' if name else ''} Sample Output\n"
        ":class: sample-output\n"
        "\n"
        "{raw-html}`"
        + (call_string + log.replace("`", "&#96;"))
        .replace("<user-input>", "<span class='user-input'>")
        .replace("</user-input>", "</span>")
        .replace("\n", "`\n{raw-html}`")
        .removesuffix("\n{raw-html}`")
        .replace("{raw-html}``", "")  # Remove empty roles.
        + "\n"
        "```\n"
    )


def format_figure(file):
    # Get the size of the image.
    if file.suffix == ".png":
        with Image.open("source" / file) as img:
            width, _ = img.size
    else:
        width = None
    up_scale = ":class: no-smoothing\n:width: 50%\n"
    return (
        "\n"
        f"```{{figure}} /{file}\n"
        f":alt: {file.name}\n" + (up_scale if width and width < 100 else "") + "\n"
        f"{file.name}\n"
        "```\n"
    )


def format_output_file(file):
    return f"\n```{{literalinclude}} /{file}\n:caption: {file.name}\n:linenos:\n```\n"
