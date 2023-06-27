import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_topics():
    """
    Returns a list of all names of course topic entries.
    """
    _, filenames = default_storage.listdir("topics")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_topic(title, content):
    """
    Saves a course topic entry, given its title and Markdown
    content. If an existing topic with the same title already exists,
    it is replaced.
    """
    filename = f"topics/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_topic(title):
    """
    Retrieves a course topic entry by its title. If no such
    topic exists, the function returns None.
    """
    try:
        f = default_storage.open(f"topics/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
