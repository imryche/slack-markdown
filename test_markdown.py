from markdown import Token, tokenize


def test_tokenizer():
    assert tokenize("") == [Token("EOF", "")]
    assert tokenize("_") == [Token("UNDERSCORE", "_"), Token("EOF", "")]
    assert tokenize("_italic") == [
        Token("UNDERSCORE", "_"),
        Token("TEXT", "italic"),
        Token("EOF", ""),
    ]
