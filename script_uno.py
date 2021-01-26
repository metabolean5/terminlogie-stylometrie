import json
import glob, re
import pprint as pp
import nltk
from nltk.tokenize import word_tokenize
import pprint as pp

articles_chrono = {}
articles_chrono["2007"] = []

for filename in sorted(glob.glob('corpusTAL/corpus/*')):
	if "2007" in filename:
		print(filename)
		file = open(filename).read()
		articles_chrono["2007"].append(file) 
pp.pprint(articles_chrono["2007"])



freq_dic = {}

for article in articles_chrono["2007"]:
	for w in word_tokenize(article, language = "french"):
		if word.lower() not in stopwords.words('french'):
			freq_dic.setdefault(word, 1)
			freq_dic[word] +=1 


print(freq_dic)








