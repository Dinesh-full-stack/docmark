import mammoth
import io
from markdownify import markdownify as md


def convert_docx_to_markdown(content: bytes) -> str:
    """
    Uses mammoth to convert .docx → HTML,
    then markdownify to convert HTML → Markdown.
    """
    with io.BytesIO(content) as f:
        result = mammoth.convert_to_html(f)
        html = result.value

    markdown = md(html, heading_style="ATX")
    return markdown.strip()
