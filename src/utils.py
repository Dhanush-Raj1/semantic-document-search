from typing import List
import re


STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "shall", "should", "may", "might", "must", "can", "could", "that",
    "this", "these", "those", "it", "its", "as", "if", "so", "not", "no",
    "nor", "than", "then", "their", "they", "them", "there", "which",
    "who", "whom", "what", "when", "where", "how", "why", "all", "each",
    "both", "few", "more", "most", "other", "some", "such", "into", "up",
    "out", "about", "also", "only", "very", "just", "any", "even", "much",
    "while", "after", "before", "through", "between", "over", "under",
    "again", "further", "once", "he", "she", "we", "you", "i", "me", "my",
    "his", "her", "our", "your", "us", "its", "well", "many", "however",
    "often", "including", "rather", "without", "across", "per", "new",
    "within", "during", "used", "make", "made", "using", "use"
}

def preprocess(text: str) -> List[str]:
    text = text.lower()

    text = re.sub(r'[^a-z\s]', '', text)

    tokens = text.split()

    tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]

    return tokens