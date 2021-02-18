import glob
from rake_nltk import Metric, Rake
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pprint as pp
import json

def extract_rake(text):
    r = Rake(language = 'fr', punctuations = ponctuation, stopwords = mots_outils)
    r.extract_keywords_from_text(text)
    pp.pprint(r.get_ranked_phrases_with_scores())
    return r.get_ranked_phrases_with_scores()

mots_outils = stopwords.words("french")
ponctuation = string.punctuation

articles = {}
for filename in sorted(glob.glob("corpusTAL/corpus/*")):
    articles[filename] = open(filename).read().lower()


rake_candidates = {"keywords":[]}

for article in articles:
    print("\n"+ str(article))
    keywords = extract_rake(articles[article])

    for w in keywords:
        if not w[1].isnumeric():
            rake_candidates["keywords"].append(w)


with open("rake_words.json", 'w', encoding='utf-8') as f:
    json.dump(rake_candidates, f, ensure_ascii=False, indent=4)


"""
for article in articles_chrono["2007"]:
    r = Rake(language = 'french', punctuations = ponctuation, stopwords = mots_outils)
    r.extract_keywords_from_text(article)
    pp.pprint(r.get_ranked_phrases_with_scores())


test = []
for filename in sorted(glob.glob("data/corpus_TALN_2007_2013/*")):
    if "2007" in filename:
        file = open(filename).readlines()
        #print(file)
        test.append(file)


rake_test = test[0][0]
r = Rake(language='french')
r.extract_keywords_from_text(rake_test)
pp.pprint(r.get_ranked_phrases_with_scores())
"""
