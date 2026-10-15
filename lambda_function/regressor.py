"""Unfinished Reddit-score regressor.

The training loop reads JSON lines (``body`` and ``score``) and the
prediction loop expects a PRAW ``reddit`` client and a ``post_id``. Neither
input is wired up. ``service.handler`` does not import this module.
"""

import json

import sklearn
from sklearn import linear_model
from sklearn.feature_extraction.text import TfidfTransformer

from StemmedCountVectorizer import StemmedCountVectorizer


class regressor:
    def __init__(self, fileName):
        comments = []
        scores = []
        for line in file:
            data = json.loads(line)
            comments.append(data["body"])
            scores.append(data["score"])
        self.vect = StemmedCountVectorizer(stop_words="english")
        self.trainer = self.vect.fit_transform(comments)
        self.tfidf = TfidfTransformer()
        self.trainer2 = self.tfidf.fit_transform(self.trainer)
        self.reducer = sklearn.feature_selection.SelectKBest(k=1000)
        reduced_data = self.reducer.fit_transform(self.trainer2, scores)
        self.reg = linear_model.BayesianRidge()
        self.reg.fit(reduced_data.toarray(), scores)

    def get_important_sentences(self):
        submission = self.reddit.submission(id=post_id)
        submission.comments.replace_more(limit=0)
        comments = []
        for comment in submission.comments:
            comments.append(comment.body)
        test = self.vect.transform(comments)
        test = self.tfidf.transform(test)
        reduced = self.reducer.transform(test)
        predictions = self.reg.predict(reduced)
        scheme = {}
        for i in range(0, len(predictions)):
            scheme[comments[i]] = predictions[i]
        return scheme
