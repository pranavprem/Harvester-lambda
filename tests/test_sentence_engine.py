"""Sentence splitting and the term-count matrix. No network."""

from sentence_engine import sentence_engine


def _engine(html="<html></html>", text=""):
    engine = sentence_engine.__new__(sentence_engine)
    engine.html = html
    engine.text = text
    return engine


def test_filter_drops_short_ruled_and_table_lines():
    lines = [
        "tiny",
        "alpha * beta gamma delta",
        "alpha | beta gamma delta",
        "alpha " * 8 + "beta gamma delta epsilon zeta",
    ]
    sentences, matrix, html = _engine(html="raw").filter(lines)
    assert html == "raw"
    assert len(sentences) == 1
    assert len(matrix) == 1
    assert len(matrix[0]) == 1
    assert matrix[0][0] == 8


def test_get_sentences_strips_non_ascii_and_splits_on_periods():
    text = "caf\u00e9 alpha alpha alpha alpha alpha alpha beta.\nno."
    sentences, matrix, _html = _engine(text=text).get_sentences()
    assert len(sentences) == 1
    assert "caf" in sentences[0]
    assert "\u00e9" not in sentences[0]
    assert matrix[0][0] >= 6


def test_get_html_drops_non_ascii(monkeypatch):
    body = "<p>caf\u00e9</p>".encode()

    class _Response:
        def read(self):
            return body

        def __enter__(self):
            return self

        def __exit__(self, *_exc):
            return False

    monkeypatch.setattr(
        "sentence_engine.urllib.request.urlopen",
        lambda url: _Response(),
    )
    assert sentence_engine("http://example.test").html == "<p>caf</p>"
