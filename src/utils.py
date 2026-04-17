from slugify import slugify


def get_slug(raw_title: str) -> str:
    return slugify(raw_title, max_length=50)
