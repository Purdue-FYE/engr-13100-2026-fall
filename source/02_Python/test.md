# PyScript: In-Browser Python Demos

This page shows how code can run directly in your browser on the static site using PyScript. No server or kernel is required.

## Quick print

<div class="pyscript-example">
  <py-script>
print("Hello from PyScript!")
  </py-script>
</div>

## Interactive greeting

Type a name and click the button — the Python function runs in your browser and updates the page.

<div class="pyscript-example">
  <input id="name" placeholder="Your name" />
  <button id="greet-btn">Greet</button>
  <div id="greet-output" style="margin-top: .5rem; font-weight: 600;"></div>

  <py-script>
from js import document
import pyscript


def greet(event=None):
    name = document.getElementById("name").value.strip()
    pyscript.write("greet-output", f"Hello, {name or 'world'}!")

# Wire up the click handler when the component loads
_document = document  # keep a reference so linter doesn't strip it
btn = _document.getElementById("greet-btn")
if btn is not None:
    btn.addEventListener("click", greet)
  </py-script>
</div>

## Live REPL

You can also execute arbitrary Python code live:

<div class="pyscript-example">
  <py-repl>
# Try editing and running this cell
import math
area = math.pi * 3**2
area
  </py-repl>
</div>

## Using the {pyscript} directive

For cleaner Markdown, authors can use the `{pyscript}` directive instead of raw HTML:

```{pyscript}
print("This code runs using the pyscript directive!")
x = 42
print(f"The answer is {x}")
```

The directive converts MyST blocks automatically into embedded `<py-script>` elements.

## More examples

Math operations:

```{pyscript}
import math
result = math.factorial(5)
print(f"5! = {result}")
```

DOM access (like the greeting example above, but using the directive):

```{pyscript}
from js import document
import pyscript

el = document.createElement("p")
el.textContent = "This paragraph was created by PyScript!"
document.body.appendChild(el)
```

```{note}
PyScript assets are loaded globally for this book via the site configuration. All `<py-script>` blocks—whether written directly in HTML or via the `{pyscript}` directive—will work on any page without additional setup.
```
