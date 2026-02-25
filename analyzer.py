import re
from collections import Counter
from utils import log_info


# Basic English stopword list for headline-style analysis
STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "of",
    "in",
    "on",
    "for",
    "to",
    "with",
    "at",
    "by",
    "from",
    "about",
    "as",
    "is",
    "are",
    "was",
    "were",
    "be",
    "this",
    "that",
    "these",
    "those",
    "it",
    "its",
    "into",
    "over",
    "under",
}


def analyze_titles(titles):
    """
    Analyze translated titles and return words repeated more than twice,
    after filtering out common English stopwords.
    """
    words = []

    for title in titles:
        clean = re.sub(r"[^\w\s]", "", title.lower())
        for token in clean.split():
            if token and token not in STOPWORDS:
                words.append(token)

    word_counts = Counter(words)
    repeated = {word: count for word, count in word_counts.items() if count > 2}

    log_info(f"Repeated words: {repeated}")
    return repeated