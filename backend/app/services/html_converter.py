from markdownify import markdownify as md
from bs4 import BeautifulSoup


def convert_html_to_markdown(html: str) -> str:
    # Parse and re-serialize to clean up malformed HTML
    soup = BeautifulSoup(html, "html.parser")
    clean_html = str(soup)
    return md(clean_html, heading_style="ATX").strip()
