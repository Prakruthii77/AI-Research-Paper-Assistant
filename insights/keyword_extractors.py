import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download("punkt")
nltk.download("stopwords")


def extract_keywords(text):
    tokens = word_tokenize(text.lower())
    sw = stopwords.words("english")
    keywords = [t for t in tokens if t.isalpha() and t not in sw]
    return list(set(keywords))