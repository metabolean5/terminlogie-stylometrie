import json
import glob, re
import pprint as pp
import nltk
from nltk.tokenize import word_tokenize
import pprint as pp
from nltk.corpus import stopwords
from sacremoses import MosesTokenizer, MosesDetokenizer
from langdetect import detect

def clean_candidates(words):
	cleaned = []
	for word in words:
		if "M   :" in word: word = word.replace("M   :", "")
		if "OTS CLÉS" in word: word = word.replace("OTS CLÉS", "")
		if "." in word: word = word.replace(".", "")
		if ":" in word: word = word.replace(":", "")
		cleaned.append(word.strip().lower())

	return cleaned
		

def moses_tokenize(text):
	mt = MosesTokenizer(lang='fr')
	return mt.tokenize(text)

def getExplicitKeyWords(text):
	prev_lang = None
	sent_tokens =  nltk.sent_tokenize(text)
	for index,sentence in enumerate(sent_tokens):
		try:
			next_lang = detect(sent_tokens[index+1])
			lang = detect(sentence)
		except:
			continue
		if lang == "fr" and prev_lang == "en" and next_lang == "en": #dans les articles du corpus, le en suivi du fr en début de fichier est une liste de mots clefs.
			return sentence.split(",") + sent_tokens[index+1].split(",")
		prev_lang = lang

	return 'No explicit key words found'

dic_key_terms = {"keywords":[]}
for filename in sorted(glob.glob('corpusTAL/corpus/*')):
	print("\n"+filename)
	candidates =  getExplicitKeyWords((open(filename).read()))

	if type(candidates) is list:
		cleaned = clean_candidates(candidates)
	else:
		print(candidates)
		continue

	print(cleaned)
	for clean in cleaned:
		dic_key_terms["keywords"].append(clean)

print(sorted(dic_key_terms["keywords"]))

with open("dic_key_terms.json", 'w', encoding='utf-8') as f:
    json.dump(dic_key_terms, f, ensure_ascii=False, indent=4)









"""
term_candidates = {}

for filename in sorted(glob.glob('corpusTAL/corpus/*')):
	term_candidates.setdefault(filename, [])

	#Tokenize
	tokens = moses_tokenize(open(filename).read())

	for t in tokens:
		print(t)
	break
"""



