"""Lambda entry point. The configured handler is service.handler."""

import json
import sys

from sentence_engine import sentence_engine
from SMMRY import SMMRY


def handler(event, context):
    """Return important fragments from the page at ``event["url"]``.

    ``CNN``, ``regressor``, and ``ensemble`` are unfinished and are not called.
    A fragment is kept only when it occurs verbatim in the fetched HTML.
    """
    engine = sentence_engine(event["url"])
    sentences, matrix, html = engine.get_sentences()
    smmry = SMMRY(sentences, matrix)
    important = smmry.get_important_sentences()
    final = []
    for imp in important:
        if imp in html:
            final.append(imp)
    return final


if __name__ == "__main__":
    event_path = sys.argv[1] if len(sys.argv) > 1 else "event.json"
    with open(event_path, encoding="utf-8") as handle:
        payload = json.load(handle)
    print(json.dumps(handler(payload, None)))
