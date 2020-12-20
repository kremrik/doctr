# docstring-to-readme
![coverage](images/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Example
Suppose you have a the following README
```
# Foo
Cool project
```

and the following Python module (`foo.py`) you want people to use
```python
"""a module to just print 'foo' as many times as you want"""

def foo(num: int):
    """A function that prints 'foo'

    Example:
        >>> from foo import foo
        >>> foo(3)
        # 'foofoofoo'
    """
    print("foo" * num)
```

You can insert the documentation for `foo.py` into your README by running
```
doctr -p /path/to/foo.py --level 2
```

which will update your README to the following
```
# Foo
Cool project

## foo
a module to just print 'foo' as many times as you want

### `foo`
A function that prints 'foo'
```python
>>> from foo import foo
>>> foo(3)
# 'foofoofoo'
```
```

## CLI
```
usage: doctr.py [-h] --path PATH [--level LEVEL] [--readme README]

optional arguments:
  -h, --help            show this help message and exit
  --path PATH, -p PATH  [REQUIRED] Path to package or module
  --level LEVEL, -l LEVEL
                        Number of '#' at top level
  --readme README, -r README
                        Path to README to update
```

## Usage
To properly format python examples in your docstrings, follow the Google-RST guide, which requires
any example block to be denoted with an `Example:` or `Examples:` block.
Any other specified blocks will be ignore, but any text at the top of the docstring will be included.
