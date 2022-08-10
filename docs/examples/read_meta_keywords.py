from luxon.html.tags import *

def read_meta_keywords(tag: Tag) -> list[str]|None:
    """Find the first meta tag that describes keywords for this HTML document and extract keywords as list

    Args:
        tag (Tag): Parent tag

    Returns:
        list[str]|None: List of keywords or None if meta keywords is not found
    """
    meta_keywords = tag.find(lambda t: type(t) == Meta and t.name == "keywords")

    if meta_keywords != None:
        content = meta_keywords.get("content")

        if content != None:
            return [t.strip().lower() for t in str(content).split(",")]

    return None