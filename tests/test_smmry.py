"""Ranking math for the sentence summarizer."""

from SMMRY import SMMRY


def test_cosine_of_identical_and_orthogonal_vectors():
    ranker = SMMRY([], [])
    assert ranker.distance([1, 0], [1, 0]) == 1
    assert ranker.distance([1, 0], [0, 1]) == 0
    assert ranker.distance([0, 0], [1, 1]) == 0


def test_central_sentence_ranks_first():
    sentences = [
        "alpha beta gamma delta epsilon zeta eta theta",
        "iota kappa lambda mu nu xi omicron pi rho sigma",
        "tau upsilon phi chi psi omega digamma stigma",
    ]
    # Row 1 is similar to both neighbors; the others only match themselves.
    matrix = [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 1],
    ]
    ranked = SMMRY(sentences, matrix).get_important_sentences()
    assert ranked[0] == sentences[1]
    assert set(ranked) == set(sentences)


def test_short_fragments_are_dropped():
    sentences = ["too short", "x" * 31]
    matrix = [[1], [1]]
    ranked = SMMRY(sentences, matrix).get_important_sentences()
    assert ranked == ["x" * 31]
