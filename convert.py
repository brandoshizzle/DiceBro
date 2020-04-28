import json
from spellList import spellList

new_dict = {}

for spellObj in spellList:
    spell_dic = json.loads(json.dumps(spellObj))
    new_name = "".join(e for e in spell_dic["name"] if e.isalnum()).lower()
    new_dict[new_name] = spell_dic
    # break

json = json.dumps(new_dict)
f = open("spellList.json", "w")
f.write(json)
f.close()
