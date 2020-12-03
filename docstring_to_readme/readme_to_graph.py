from docstring_to_readme.graph import node


def loads(readme: str) -> dict:
    if not readme:
        return {}

    if not readme.lstrip().startswith("#"):
        return {}

    lines = readme.strip().split("\n")

    for line in lines:
        if line.startswith("#"):
            pass


def load():
    pass
