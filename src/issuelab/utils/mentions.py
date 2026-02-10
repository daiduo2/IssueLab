"""Shared mention parsing helpers."""

import re

# GitHub username pattern: alnum/underscore, can include internal hyphen/underscore.
GITHUB_MENTION_PATTERN = re.compile(r"@([a-zA-Z0-9_](?:[a-zA-Z0-9_-]*[a-zA-Z0-9_])?)")


def extract_github_mentions(text: str | None) -> list[str]:
    """Extract deduplicated @mentions while preserving order."""
    if not text:
        return []

    matches = GITHUB_MENTION_PATTERN.findall(text)

    seen: set[str] = set()
    result: list[str] = []
    for username in matches:
        if username not in seen:
            seen.add(username)
            result.append(username)
    return result


def extract_controlled_mentions(text: str | None) -> list[str]:
    """Extract mentions only from controlled collaboration sections.

    Supported formats:
    - `相关人员: @alice @bob`
    - `协作请求:` followed by bullet lines like `- @alice`
    """
    if not text:
        return []

    result: list[str] = []
    seen: set[str] = set()
    in_list_section = False

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if "相关人员:" in line:
            suffix = line.split("相关人员:", 1)[1]
            for username in extract_github_mentions(suffix):
                if username not in seen:
                    seen.add(username)
                    result.append(username)
            in_list_section = False
            continue

        if line.startswith("协作请求:"):
            in_list_section = True
            continue

        if in_list_section:
            if re.match(r"^\s*-\s+@", raw_line):
                for username in extract_github_mentions(raw_line):
                    if username not in seen:
                        seen.add(username)
                        result.append(username)
                continue
            if line and not line.startswith("-"):
                in_list_section = False

    return result
