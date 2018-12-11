# -*- coding: utf-8 -*-
"""Handler function to service lambda
"""
from sentence_engine import sentence_engine
from SMMRY import SMMRY


def handler(event, context):
    engine = sentence_engine(event["url"])
    sentences, matrix, html = engine.get_sentences()
    smmry = SMMRY(sentences,matrix)
    cnn = cnn(sentences,matrix)
    regressor = regressor(sentences, matrix)
    important = smmry.get_important_sentences()
    important.extend(cnn.get_important_sentences())
    important.extend(regressor.get_important_sentences())
    important.extend(ensemble.get_important_sentences())
    final = []
    for imp in important:
        if imp in html:
            final.append(imp)
    return final
        