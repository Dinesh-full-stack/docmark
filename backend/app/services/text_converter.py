import re


def convert_text_to_markdown(text: str) -> str:
    """
    Heuristic plain-text to Markdown conversion:
    - ALL CAPS lines           → H2 headings
    - Lines starting with -, *, • → unordered list
    - Lines starting with 1. 2. etc → ordered list
    - Indented lines (4 spaces or tab) → fenced code block
    - Everything else          → plain paragraph text
    """
    lines = text.splitlines()
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Preserve empty lines as paragraph breaks
        if not stripped:
            result.append("")
            i += 1
            continue

        # ALL CAPS line → heading
        if stripped == stripped.upper() and len(stripped) > 3 and not stripped.startswith("-"):
            result.append(f"## {stripped.title()}")
            i += 1
            continue

        # Unordered list
        if re.match(r"^[-*•]\s+", stripped):
            result.append(f"- {stripped.lstrip('-*•').strip()}")
            i += 1
            continue

        # Ordered list
        if re.match(r"^\d+[\.\)]\s+", stripped):
            num = re.match(r"^(\d+)", stripped).group(1)
            content = re.sub(r"^\d+[\.\)]\s+", "", stripped)
            result.append(f"{num}. {content}")
            i += 1
            continue

        # Indented block → fenced code
        if line.startswith("    ") or line.startswith("\t"):
            code_lines = []
            while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("\t")):
                code_lines.append(lines[i].lstrip())
                i += 1
            result.append("```")
            result.extend(code_lines)
            result.append("```")
            continue

        # Default: plain paragraph text
        result.append(stripped)
        i += 1

    return "\n".join(result)
