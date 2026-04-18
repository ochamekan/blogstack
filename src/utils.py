from slugify import slugify
from sqlalchemy.exc import IntegrityError
import re


def get_slug(raw_title: str) -> str:
    return slugify(raw_title, max_length=50)


def get_constraint_name_from_integrity_error(exc: IntegrityError) -> str | None:
    """Extract constraint name from SQLAlchemy IntegrityError with asyncpg. Can't find any info in official docs so i vibecoded it"""
    for candidate in (
        exc.orig,
        getattr(exc.orig, "__cause__", None),
        getattr(exc.orig, "__context__", None),
    ):
        if candidate is None:
            continue
        constraint = getattr(candidate, "constraint_name", None)
        if constraint:
            return constraint

        diag = getattr(candidate, "diag", None)
        if diag and hasattr(diag, "constraint_name"):
            return diag.constraint_name

    match = re.search(r'constraint "([^"]+)"', str(exc))
    return match.group(1) if match else None
