"""Handler contract: a list of fragments that occur in the fetched HTML."""

from service import handler


class _Response:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False


def test_handler_returns_html_substrings(monkeypatch):
    sentence = "alpha " * 12 + "beta gamma delta epsilon zeta theta iota kappa"
    body = f"<html><body><p>{sentence}.</p></body></html>"
    monkeypatch.setattr(
        "sentence_engine.urllib.request.urlopen",
        lambda url: _Response(body.encode("utf-8")),
    )

    result = handler({"url": "http://example.test/page"}, None)

    assert result == [sentence]


def test_handler_requires_url():
    try:
        handler({}, None)
    except KeyError as exc:
        assert exc.args == ("url",)
    else:
        raise AssertionError("expected KeyError")
