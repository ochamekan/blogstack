def get_slug(raw_title: str) -> str:
    return "-".join(raw_title.lower().split(" "))
