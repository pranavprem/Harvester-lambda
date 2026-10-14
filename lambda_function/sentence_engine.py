"""Fetch a URL and turn the page into sentences plus a term-count matrix."""

import os
import urllib.request

import html2text
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

# Data shipped next to this module (local checkout and the Lambda zip), plus
# the historical path used when the zip root was mounted at /.
_BUNDLED_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nltk_data")
if os.path.isdir(_BUNDLED_DATA):
    nltk.data.path.append(_BUNDLED_DATA)
nltk.data.path.append("/nltk_data")


class sentence_engine:
    """Download a page and build a bag-of-words matrix of its sentences."""

    def __init__(self, url):
        self.html = self.get_html(url)
        self.text = ""
        self.get_text()

    def get_text(self):
        """Convert the fetched HTML to plain text."""
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.bypass_tables = True
        text_maker.ignore_images = True
        text_maker.ignore_emphasis = True
        text_maker.escape_snob = 1
        self.text = text_maker.handle(self.html)

    def get_html(self, url):
        """Return the page body as ASCII, dropping non-ASCII characters."""
        with urllib.request.urlopen(url) as response:
            html = response.read()
        encoded_html = html.decode("utf-8")
        return encoded_html.encode("ascii", "ignore").decode("ascii")

    def filter(self, lines):
        """Keep long plain lines and build a count matrix of the top terms."""
        stop_words = set(stopwords.words("english"))
        toks = []
        token_map = {}
        sentences = {}
        matrix = []
        bag = set()
        for line in lines:
            if len(line) > 5 and "*" not in line and "|" not in line:
                tokens = word_tokenize(line)
                tokens = [w.lower() for w in tokens]
                tokens = [word for word in tokens if word.isalpha()]
                tokens = [w for w in tokens if w not in stop_words]
                toks.extend(tokens)
                sentences[line] = tokens
        for token in set(toks):
            if toks.count(token) > 5:
                token_map[token] = toks.count(token)
        token_map = sorted(token_map.items(), key=lambda kv: kv[1], reverse=True)

        for key, _value in token_map[:20]:
            bag.add(key)

        for line in sentences:
            temp = []
            for word in bag:
                temp.append(sentences[line].count(word))
            matrix.append(temp)
        return list(sentences.keys()), matrix, self.html

    def get_sentences(self):
        """Split the plain text on periods and return sentences, matrix, HTML."""
        lines = (
            self.text.encode("ascii", "ignore")
            .decode("ascii")
            .replace("\n", " ")
            .split(".")
        )
        return self.filter(lines)
