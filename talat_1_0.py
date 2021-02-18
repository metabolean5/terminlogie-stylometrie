import json
import glob, re
import pprint as pp
from rake_nltk import Metric, Rake
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class Talat:

    betbotCount = 0

    def __init__(
        self,
        ):

    	self.all_terms = None

    def runExtractionArticle(self,res,text):

    	global morph_dic
    	grammaire = ["un", "une", "des", "les", "pour", "par", "dans", "vers", "pendant", "depuis" , "malgé", "comme", "contre", "ci", "selon", ]

    	def isGrammar(word):

    		if word in morph_dic["adjectif"]:
    			return False
    		if word in morph_dic["grammaire"]:
    			return True
		

    	mots_outils = stopwords.words("french")
    	ponctuation = string.punctuation
    	r = Rake(language = 'fr', punctuations = ponctuation, stopwords = mots_outils)
    	r.extract_keywords_from_text(text)

    	for index, candidate in enumerate(r.get_ranked_phrases_with_scores()):

    		new_candidate = candidate[1]
    		good_candidate = True

    		if len(candidate[1].split(' '))<2:
    			good_candidate = False

    		i=0
    		for w in candidate[1].split(' '):

    			if i==0 and (w in morph_dic["adverbe"] or w in morph_dic["adjectif"]):
    				good_candidate = False
    				break

    			if isGrammar(w):
    				good_candidate = False
    				break

    			if w in grammaire:
    				good_candidate = False
    				break

    			if (w in string.punctuation or (w in ["’","«", "»", "»", "»"])):
    				new_candidate = new_candidate.replace(w,"")
    				continue

    			for p in string.punctuation:
    				if p in w:
    					new_candidate = new_candidate.replace(p,"")
    			i+=1

    		if good_candidate:
    			res[new_candidate.strip()] = ''


    	return res

    def extractTermsArticle(self,article, dic):
    	print("treating article with length " + str(len(article)))

    	for kw in self.all_terms:
    		if kw in article:
    			dic.setdefault(kw,0)
    			dic[kw] += article.count(kw)

    	return dic

    def countOccurenceCorpus(self,corpus):
    	all_terms_freq = {}

    	for filename in sorted(glob.glob(corpus)):
    		print("\n"+filename)
    		file = open(filename)
    		curr_article = file.read().lower()

    		for kw in self.all_terms:
    			all_terms_freq.setdefault(kw,0)
    			all_terms_freq[kw] += curr_article.count(kw)

    		file.close()

    	return all_terms_freq

    def countOccurenceYear(self,corpus):

    	year_terms_freq = {}

    	for filename in sorted(glob.glob(corpus)):
    		print(filename)
    		year = filename.split('-')[1]
    		file = open(filename)
    		article = file.read().lower()
    		year_terms_freq.setdefault(year,{})

    		for kw in self.all_terms:
    			year_terms_freq[year].setdefault(kw,0)
    			year_terms_freq[year][kw] += article.count(kw)
    		
    		file.close()

    	return year_terms_freq

    def growth_rate(self,freq_voc1, freq_voc2):
    	growth_dic = {}
    	for w in freq_voc1:
    		print(w)
    		if w in freq_voc2 and w in freq_voc1 :
    			growth_dic[w] = freq_voc2[w] / freq_voc1[w]
    		elif w not in freq_voc1:
    			growth_dic[w] = 100000
    		elif w not in freq_voc2:
    			growth_dic[w] = 0

    	for w in freq_voc2:
    		if w not in freq_voc1:
    			growth_dic[w] = 100000

    	return growth_dic


#INITIALIZE TALAT
print("INITIALIZING TALAT")
with open('rake_kw.json') as outfile:
    rake_kw = json.load(outfile)

with open('explicit_kw.json') as outfile:
    explicit_kw = json.load(outfile)

with open('corpus_reference.json') as outfile:
    corp_ref = json.load(outfile)

global morph_dic
with open('morph_dic.json') as outfile:
    morph_dic = json.load(outfile)



#extraction d'unités terminologiques polylexicales

talat = Talat()

res = {}

for filename in sorted(glob.glob("corpusLQ/*")):
	print("\n"+filename)
	file = open(filename)
	curr_article = file.read().lower()
	res = talat.runExtractionArticle(res,curr_article)

pp.pprint(res)




#CORPUS TALN COURS LEJEUNE

"""
all_terms_dic = {}

for kw in explicit_kw:
	all_terms_dic[kw] = ''

for kw in rake_kw:
	all_terms_dic[kw] = ''

talat = Talat(all_terms_dic)

print("LOADED TALAT")

"""



























"""
#Récupération des termes sur un seul article pour évalutation du système Talat
curr_article = open("corpusTAL/corpus/recital-2007-long-001").read()
test_article_kw = talat.extractTermsArticle(curr_article)

missing1 = []
for kw in test_article_kw:
	if kw not in corp_ref:
		missing1.append(kw)

print("\n")
print("Evalutation TALAT sur corpus de ref: "+ str(len(missing1)/len(corp_ref)))
print("TALAT DONE")

pp.pprint(missing1)

"""
"""
#Statistiques fréquences sur corpus en entier
all_terms_freq = talat.countOccurenceCorpus("corpusTAL/corpus/*")
pp.pprint(sorted(all_terms_freq.items(), key = lambda item : item[1]))
"""

#statistiques corpus fréquences par années
"""
year_freq =  talat.countOccurenceYear("corpusTAL/corpus/*")

with open("years_terms_freq.json", 'w', encoding='utf-8') as f:
    json.dump(year_freq, f, ensure_ascii=False, indent=4)


pp.pprint(year_freq)




with open('years_terms_freq2.json') as outfile:
    year_freq_new = json.load(outfile)


year_freq_new ={}
for year in year_freq:
	year_freq_new.setdefault(year,{})
	for kw in year_freq[year]:
		if year_freq[year][kw] >= 2:
			year_freq_new[year][kw] = year_freq[year][kw]
			

with open("years_terms_freq2.json", 'w', encoding='utf-8') as f:
    json.dump(year_freq_new, f, ensure_ascii=False, indent=4)
""

for year in year_freq_new:
	print(year)
	pp.pprint(sorted(year_freq_new[year].items(), key = lambda item : item[1]))


gr_07_08 = talat.growth_rate(year_freq_new["2007"],year_freq_new["2008"])
pp.pprint(sorted(gr_07_08.items(), key = lambda item : item[1]))




kw_detected_articles = {}
for filename in sorted(glob.glob('corpusTAL/corpus/*')):
	print("\n"+filename)
	curr_article = open(filename).read()

	kw_detected_articles[filename] = talat.extractTermsArticle(curr_article)
	break

print(kw_detected_articles)

"""



