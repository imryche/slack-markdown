import re
from dataclasses import dataclass, field


@dataclass
class Paragraph:
    raw: str
    nodes: list = field(default_factory=lambda: [])


@dataclass
class Blockquote:
    raw: str


@dataclass
class List:
    raw: str
    nodes: list = field(default_factory=lambda: [])


@dataclass
class ListItem:
    raw: str


class NL:
    pass


@dataclass
class Text:
    value: str


@dataclass
class Bold:
    value: str


@dataclass
class Italic:
    value: str


def parse_document(markdown):
    prev, curr = None, None
    buf = []
    lines = markdown.split("\n")
    for line in lines:
        if re.match(r"^ *\d+. ", line):
            curr = List
        else:
            curr = Paragraph

        if prev and curr != prev:
            yield prev(raw="\n".join(buf))
            buf = []

        buf.append(line)
        prev = curr

    yield curr(raw="\n".join(buf))


def parse_line(line, nodes=None):
    if not nodes:
        nodes = []

    if match := re.match(r"^\*([^\*]+)\*", line):
        nodes.append(Bold(value=match.group(1)))
        parse_line(line[match.end() :], nodes)

    if match := re.match(r"^_([^_]+)_", line):
        nodes.append(Italic(value=match.group(1)))
        parse_line(line[match.end() :], nodes)

    elif match := re.match(r"^([^\*_]+)", line):
        nodes.append(Text(value=match.group(1)))
        parse_line(line[match.end() :], nodes)

    return nodes


def parse_paragraph(paragraph):
    nodes = []
    lines = paragraph.raw.split("\n")
    for line in lines:
        nodes.extend(parse_line(line))
        if line != lines[-1]:
            nodes.append(NL())

    paragraph.nodes = nodes
    return paragraph


def parse_list(list_):
    prev_indent = 0
    buf = []
    for line in list_.raw.split("\n"):
        match = re.match("^( *)", line)
        indent = len(match.group(1))

        if indent == 0 and prev_indent != 0:
            print(buf)
            buf = []

        buf.append(line)
        prev_indent = indent


def parse(markdown):
    nodes = []
    for block in parse_document(markdown):
        if isinstance(block, Paragraph):
            block = parse_paragraph(block)
            nodes.append(block)
        elif isinstance(block, Blockquote):
            pass
        elif isinstance(block, List):
            block = parse_list(block)

    return nodes
