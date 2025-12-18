"""
PyScript Sphinx directive

Provides a {pyscript} directive that converts MyST blocks into embedded PyScript
<py-script> HTML elements.

Usage in MyST/Markdown:
    ```{pyscript}
    print("Hello from PyScript!")
    ```

This generates:
    <py-script>print("Hello from PyScript!")</py-script>
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import unchanged


class PyScriptDirective(Directive):
    """
    A Sphinx directive for embedding PyScript code blocks.
    
    Converts MyST {pyscript} blocks into <py-script> HTML elements
    that run Python code directly in the browser.
    """

    has_content = True
    option_spec = {
        "class": unchanged,
        "linenos": unchanged,
    }
    required_arguments = 0
    optional_arguments = 0

    def run(self):
        """Generate raw HTML containing a <py-script> block."""
        code = "\n".join(self.content)
        
        # Build the raw HTML node
        html_code = f"<py-script>\n{code}\n</py-script>"
        raw_node = nodes.raw("", html_code, format="html")
        
        return [raw_node]


def setup(app):
    """Register the directive with Sphinx."""
    app.add_directive("pyscript", PyScriptDirective)
    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


# When used as a confextras extension, Sphinx will call setup()
__all__ = ["setup"]
