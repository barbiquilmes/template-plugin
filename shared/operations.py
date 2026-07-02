"""Shared helpers used by more than one plugin in this marketplace.

This file lives at the marketplace root, OUTSIDE any plugin subdirectory.
A plugin can only use it through a symlink inside its own directory
(see plugins/txt-demo/shared) — on install, Claude Code dereferences the
symlink and copies this content into the plugin's cache directory.
"""


def count_words(text: str) -> dict:
    """Return line, word, and character counts for a piece of text."""
    words = text.split()
    lines = text.splitlines()
    return {
        "line_count": len(lines),
        "word_count": len(words),
        "char_count": len(text),
    }
