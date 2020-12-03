from typing import List, Optional


def section(
    heading: str,
    body: str,
    pretty_heading: Optional[str] = "",
) -> dict:
    return {
        "heading": heading,
        "pretty_heading": pretty_heading or heading,
        "body": body,
    }


# ---------------------------------------------------------


def readme_to_sections(
    readme: str,
) -> List[Optional[dict]]:
    lines = [line.strip() for line in readme.split("\n")]
    sections = []

    _sections = []
    section_parts = None

    for line in lines:
        if line.startswith("#"):
            if section_parts:
                _sections.append(section_parts)
            section_parts = []
            section_parts.append(line)
        else:
            section_parts.append(line)

    if section_parts:
        _sections.append(section_parts)

    for s in _sections:
        heading = s[0]
        body = "\n".join(s[1:])
        sections.append(section(heading, body))

    return sections


def sections_to_readme(
    sections: List[Optional[dict]],
) -> str:
    readme = ""

    for section in sections:
        heading = section["heading"]  # should be function
        body = section["body"]
        sep = "\n" if body else ""
        str_sect = heading + sep + body

        if readme:
            readme = readme + "\n" + str_sect
        else:
            readme = str_sect

    return readme
