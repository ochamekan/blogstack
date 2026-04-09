import re


def get_reading_time(body: str) -> int:
    text = re.sub(r"```.*?```", "", body, flags=re.DOTALL)  # fenced code blocks
    text = re.sub(r"`[^`]+`", "", text)  # inline code
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)  # images
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)  # links
    text = re.sub(r"#{1,6}\s+", "", text)  # headings
    text = re.sub(r"[*_~`>|]", "", text)  # emphasis, blockquotes, tables

    words = len(text.split())
    return max(1, round(words / 200))
