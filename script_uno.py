import json
import glob, re
import pprint as pp
import nltk
from nltk.tokenize import word_tokenize
import pprint as pp
from nltk.corpus import stopwords

def compute_freqdic(articles_chrono, year):
	for article in articles_chrono[year]:
		print("article proceseed")
		for w in word_tokenize(article, language = "french"):
			if w.lower() not in stopwords.words('french'):
				freq_dic[year].setdefault(w, 1)
				try:
					freq_dic[year][w] +=1
				except:
					continue
	return freq_dic

def growth_rate(freq_voc1, freq_voc2):
	growth_dic = {}
	for w in freq_voc1:
		print(w)
		if w in freq_voc2 and w in freq_voc1 :
			growth_dic[w] = freq_voc2[w] / freq_voc1[w]
		elif w not in freq_voc2:
			growth_dic[w] = 0
		elif w not in freq_voc1:
			growth_dic[w] = 100000
	return growth_dic


def returnTopFreq(freq_dic):

	for year in freq_dic:
		print("\nFREQUENCIES FOR YEAR : "+ year)
		sorteddic = sorted(freq_dic[year].items(), key=lambda item: item[1])
		pp.pprint(sorteddic)


articles_chrono = {"2007":[], "2008": []}

#build chronological dic
for filename in sorted(glob.glob('corpusTAL/corpus/*')):

	if "2007" in filename:
		print(filename)
		file = open(filename).read()
		articles_chrono["2007"].append(file)

	if "2008" in filename:
		print(filename)
		file = open(filename).read()
		articles_chrono["2008"].append(file) 

print(articles_chrono["2007"][0])
freq_dic = {"2007":{},"2008":{}}
freq_dic = compute_freqdic(articles_chrono,"2007")
freq_dic = compute_freqdic(articles_chrono,"2008")

returnTopFreq(freq_dic)
print("('suce moi les boules', 12508493)]")


'''
#print("frequency computed")

growth_dic = growth_rate(freq_dic["2007"], freq_dic["2008"])
fonction
growth_dic = sorted(growth_dic.items(), key=lambda item: item[1])

print(growth_dic)


'''
