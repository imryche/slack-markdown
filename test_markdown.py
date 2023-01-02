from pprint import pprint

import pytest

from markdown import List, Paragraph, parse, parse_document


@pytest.mark.skip
def test_parse_document():
    markdown = (
        "a *paragraph* _containing_ text\n"
        "on multiple lines.\n"
        "\n"
        "1. first item\n"
        "2. second item"
    )
    nodes = list(parse_document(markdown))
    assert nodes == [
        Paragraph(raw=("a *paragraph* _containing_ text\non multiple lines.\n")),
        List(raw=("1. first item\n2. second item")),
    ]


def test_parse():
    text = (
        "a *paragraph* _containing_ text\n"
        "on multiple lines.\n"
        "\n"
        "1. first item\n"
        "   1. sub item first\n"
        "2. second item\n"
        "   1. sub item second\n"
    )
    pprint(parse(text))
