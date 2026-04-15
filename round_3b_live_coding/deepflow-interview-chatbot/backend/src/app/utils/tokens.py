"""Token counting utilities using tiktoken.

Provides accurate token estimation via the cl100k_base encoding (used by
GPT-4, Claude via OpenRouter, and most modern LLMs on OpenRouter).
"""

import logging

import tiktoken

logger = logging.getLogger(__name__)

_encoding = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """Count the exact number of tokens in a string using cl100k_base."""
    if not text:
        return 0
    return len(_encoding.encode(text))


def truncate_to_token_budget(text: str, max_tokens: int) -> str:
    """Truncate text to fit within a token budget.

    Returns the original text if within budget, otherwise truncates at a
    token boundary and appends a trailing indicator.
    """
    tokens = _encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text

    suffix = "\n\n[... truncated ...]"
    suffix_tokens = _encoding.encode(suffix)
    budget = max_tokens - len(suffix_tokens)

    if budget <= 0:
        return suffix

    truncated = _encoding.decode(tokens[:budget])

    last_newline = truncated.rfind("\n")
    if last_newline > len(truncated) * 0.8:
        truncated = truncated[:last_newline]

    logger.info(
        "truncated text from %d to ~%d tokens",
        len(tokens),
        count_tokens(truncated),
    )
    return truncated + suffix
