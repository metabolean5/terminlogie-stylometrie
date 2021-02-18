import pprint as pp
import json
import string
import sys

def isConjugaison(word):

	if word in morph_dic["adjectif"]:
		return False
	if word in morph_dic["grammaire"]
	return False
		

with open('morph_dic.json') as outfile:
    morph_dic = json.load(outfile)

with open('rake_words.json') as outfile:
    rake_words = json.load(outfile)


rake_words_2 = {"keywords": []}

grammaire = ["un", "une", "des", "les", "pour", "par", "dans", "vers", "pendant", "depuis" , "malgé"]


for index, candidate in enumerate(rake_words["keywords"]):

	new_candidate = candidate[1]
	good_candidate = True

	if len(candidate[1].split(' '))<2:
		good_candidate = False


	for w in candidate[1].split(' '):

		print(w)

		if isConjugaison(w):
			good_candidate = False
			break

		if w in grammaire:
			good_candidate = False
			break

		if (w in string.punctuation or (w in ["«", "»", "»", "»"])):
			new_candidate = new_candidate.replace(w,"")
			continue

		for p in string.punctuation:
			if p in w:
				new_candidate = new_candidate.replace(p,"")


	print(new_candidate)

	if good_candidate:
		rake_words_2["keywords"].append(new_candidate.strip())

	print("progession : "+  str(index) + "/"+ str(len(rake_words["keywords"])) + " current term = "+ new_candidate)

rake_words_2["keywords"] = list(set(rake_words_2["keywords"]))

with open("rake_words_4.json", 'w', encoding='utf-8') as f:
    json.dump(rake_words_2, f, ensure_ascii=False, indent=4)








