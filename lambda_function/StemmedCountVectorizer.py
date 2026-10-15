"""CountVectorizer that stems tokens with the English Snowball stemmer.

Used only by the unfinished ``regressor`` module. Importing this module
imports scikit-learn, which is not part of the Lambda runtime install.
"""

import nltk
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")


class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        analyzer = super().build_analyzer()
        return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])
