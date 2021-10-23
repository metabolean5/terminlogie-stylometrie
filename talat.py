import json
import glob, re
import pprint as pp
from rake_nltk import Metric, Rake
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import sys

class Talat:

    def __init__(
        self,
        ):

    	self.all_terms = None

    def setAllTerms(self,all_terms):
        self.all_terms = all_terms

    def runExtractionArticle(self,res,text):

        global morph_dic
        grammaire = ["ainsi","ces","ce", "ceux", "celles", "cet", "cette", "aucun","un", "une", "les", "pour", "par", "dans", "vers", "pendant", "depuis" , "malgé", "comme", "contre", "ci", "selon", "parce", "grâce", "surtout", "afin", "tel", "telles", "tels", "telle"]

        ending_grammaire = ["du", "des", "de"]

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

                if i==(len(candidate[1].split(' '))-1) and (w in ending_grammaire):
                    good_candidate = False
                    break

                if isGrammar(w):
                    good_candidate = False
                    break

                if w in grammaire:
                    good_candidate = False
                    break

                if (w in string.punctuation or (w in ["\uf0b7","▪","’","«", "»", "»", "»"])):
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

    def growth_rate(self,freq_voc1,freq_voc2):
        growth_dic = {}
        for w in freq_voc1:
            print(w)
            if freq_voc1[w] != 0:
                growth_dic[w] = freq_voc2[w] / freq_voc1[w]
                continue
            if freq_voc2[w] == 0:
                growth_dic[w] = 0
                continue
            if freq_voc2[w] > 0 and freq_voc1[w] == 0:
                growth_dic[w] = 100000
                continue


        return growth_dic


if __name__ == '__main__':
   

    #INITIALIZE TALAT
    print(open('talatlogo.txt').read())
    global morph_dic
    with open('morph_dic.json') as outfile:
        morph_dic = json.load(outfile)

    talat = Talat()

    #extraction d'unités terminologiques polylexicales

    corpuspath = sys.argv[1]

    #iteration sur le corpus et extraction des termes
    res = {}
    for filename in sorted(glob.glob(corpuspath)):
        print("\n"+filename)
        file = open(filename)
        curr_article = file.read().lower()
        res = talat.runExtractionArticle(res,curr_article)
        file.close()


    with open("termes.json", 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)

    talat.setAllTerms(res) #attribut une liste de termes pour talat


    for candidat in list(talat.all_terms): #cleaning
        if len(candidat) <= 1 or candidat.isnumeric():
            talat.all_terms.pop(candidat, None)

    print(talat.all_terms)



""""
input("\nLaunch term occurence count on corpus ?")


occ_terms = talat.countOccurenceCorpus('corpusERDYN-PEPR/fondo/*')


with open("allterms_pepr.json", 'w', encoding='utf-8') as f:
    json.dump(occ_terms, f, ensure_ascii=False, indent=4)



occ_terms = pd.DataFrame(occ_terms.items(), columns=['Term', 'Occurences'])

print(occ_terms)

pp.pprint(occ_terms.sort_values( by = ['Occurences']).to_string())

"""


"""
#Calcule du growth rate pour chque termes sur une fenetre par années
occ_years_dic = talat.countOccurenceYear('corpus/corpusLQ/*')


with open("occ_years_dic .json", 'w', encoding='utf-8') as f:
    json.dump(occ_years_dic, f, ensure_ascii=False, indent=4)


with open('occ_years_dic.json') as outfile:
    occ_years_dic = json.load(outfile)

growth_dic_years = {}
for year in range(2007,2013):
    year = str(year)
    if year == "2013":
        break
    print(year)
    growth_dic_years[year + " " + str(int(year)+1)] =  talat.growth_rate(occ_years_dic[year], occ_years_dic[str(int(year)+1)])


with open("growth_dic_years.json", 'w', encoding='utf-8') as f:
    json.dump(growth_dic_years, f, ensure_ascii=False, indent=4)

with open('growth_dic_years.json') as outfile:
    growth_dic_years = json.load(outfile)

with open('termes.json') as outfile:
    termes = json.load(outfile)


#nouvelle représentation du growth rate mais en fonction des termes
termes_gr_years = {}

for t in termes:
    print(t)
    termes_gr_years[t] = {}
    for gr_years in growth_dic_years:
        termes_gr_years[t][gr_years] = growth_dic_years[gr_years][t]

with open("termes_gr_years.json", 'w', encoding='utf-8') as f:
    json.dump(termes_gr_years, f, ensure_ascii=False, indent=4)

with open('termes_gr_years.json') as outfile:
    termes_gr_years = json.load(outfile)


#extraction des termes qui apparaissent puis ont un fréquence stable
emerging_concepts = {}
for t in termes_gr_years:
    rates = []
    for year_pairs in termes_gr_years[t]:
        rates.append(termes_gr_years[t][year_pairs])

    b = False
    if rates.count(100000) == 1 and all_terms_freq[t] > 20:
        b = True
        index = rates.index(100000)
        for gr in rates[index:]:
            if gr == 0:
                b = False
        for gr in rates[:index]:
            if gr > 0:
                b = False

    if b == True:
        emerging_concepts[t] = termes_gr_years[t]

  
pp.pprint(emerging_concepts)


articles_year = {}

for filename in sorted(glob.glob("corpus/corpus/*")):
    print(filename)
    year = filename.split('-')[1]
    file = open(filename)
    article = file.read().lower()
    articles_year.setdefault(year,0)
    articles_year[year] += len(article)

print(articles_year)





with open('termes.json') as outfile:
    res = json.load(outfile)
talat.setAllTerms(res)

#Growth rate examination
occ_years_dic = talat.countOccurenceYear('corpus/corpus/*')

with open("occ_years_dic .json", 'w', encoding='utf-8') as f:
    json.dump(occ_years_dic, f, ensure_ascii=False, indent=4)




growth_dic_years = {}
for year in occ_years_dic:
    if year == "2013":
        break

    print(year)
    growth_dic_years[year + " " + str(int(year)+1)] =  talat.growth_rate(year, str(int(year)+1))

pp.pprint(growth_dic_years)




















#CORPUS TALN COURS LEJEUNE


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



