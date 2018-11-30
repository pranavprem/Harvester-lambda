# -*- coding: utf-8 -*-
"""Handler function to service lambda
"""
from sentence_engine import sentence_engine



def handler(event, context):
    engine = sentence_engine(event["url"])
    return engine.get_sentences()