# docstring-to-readme
![coverage](images/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

#### Function [`file_as_ast`](./docstring_to_readme/parser.py#L8)
Function to convert a file to an AST object

#### Function [`module_to_sections`](./docstring_to_readme/parser.py#L18)
Function to convert an AST module to Markdown sections

```python
>>> from docstring_to_readme.parser import module_to_sections
>>> import ast
>>> module = ast.parse("def fnc():\n    '''hello'''\n    pass")
>>> module_to_sections(module)
'#### `fnc`\nhello'
```
