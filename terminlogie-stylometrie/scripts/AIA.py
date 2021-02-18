
import json

f_martial = open("annotation_kw_l2007_1").readlines()
f_virgile = open("annotations_virgile.txt").readlines()

#calcul de l'AIA

kw_martial = {}
kw_virgile = {}

for t in f_martial:
	kw_martial[t.strip().lower()] = ""

for t in f_virgile:
	kw_virgile[t.strip().lower()] =""


print('\n')

missing = []
for kw in kw_virgile:
	if kw not in kw_martial:
		missing.append(kw)

corp_ref = {**kw_martial, **kw_virgile}


print(missing)
print(len(missing))

print("AIA kw_virgile/kw_martial : "+ str(1 - len(missing)/len(kw_virgile)))

missing = []
for kw in kw_martial:
	if kw not in kw_virgile:
		missing.append(kw)

with open("explicit_kw.json", 'w', encoding='utf-8') as f:
    json.dump(ex_key_dic, f, ensure_ascii=False, indent=4)


print(missing)
print(len(missing))

print("AIA kw_virgile/kw_martial : "+ str(1 - len(missing)/len(kw_martial)))

with open("corpus_reference.json", 'w', encoding='utf-8') as f:
    json.dump(corp_ref, f, ensure_ascii=False, indent=4)
