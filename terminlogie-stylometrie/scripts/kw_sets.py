import pprint as pp
import json
import string
import sys
import re

def removeExtraWhite(term):
	newterm = term

	if "     " in term:
		newterm = re.sub('     ', ' ', newterm)

	if "    " in term:
		newterm = re.sub('    ', ' ', newterm)
		
	if "   " in term:
		newterm = re.sub('   ', ' ', newterm)
		
	if "  " in term:
		newterm = re.sub('  ', ' ', newterm)

	return newterm

with open('dic_key_terms.json') as outfile:
    explicit_keys = json.load(outfile)

with open('rake_words_4.json') as outfile:
    rake_words = json.load(outfile)

ex_key_dic = {}
rkw_dic = {}

for ex_key in explicit_keys["keywords"]:
	if len(ex_key.split(' '))> 2: 
		ex_key_dic[removeExtraWhite(ex_key)] = ""

for rkw in rake_words["keywords"]:

	if len(rkw.split(' '))> 2: 
		rkw_dic[removeExtraWhite(rkw)] = ""


with open("rake_kw.json", 'w', encoding='utf-8') as f:
    json.dump(rkw_dic, f, ensure_ascii=False, indent=4)


with open("explicit_kw.json", 'w', encoding='utf-8') as f:
    json.dump(ex_key_dic, f, ensure_ascii=False, indent=4)

	

missing = []
for ex_key in ex_key_dic:
	if ex_key not in rkw_dic:
		missing.append(ex_key)





print(str(len(missing)))
print(str(len(ex_key_dic)))
print(str(len(missing) / len(ex_key_dic)))

print(missing)
