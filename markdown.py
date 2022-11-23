import re
from collections import namedtuple

Token = namedtuple("Token", "type value")


def tokenize(markdown, tokens=None):
    if not tokens:
        tokens = []

    if not markdown:
        tokens.append(Token("EOF", ""))
        return tokens

    match = re.match(r"^_", markdown)
    if match:
        tokens.append(Token("UNDERSCORE", "_"))
        return tokenize(markdown[match.end() :], tokens)

    match = re.match(r"(.+)", markdown)
    if match:
        tokens.append(Token("TEXT", match.group(1)))
        return tokenize(markdown[match.end() :], tokens)

    raise ValueError(f"Couldn't match given input {markdown}")
