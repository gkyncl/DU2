import math, json, quad_tree

# nacteni geoJSON souboru

with open("points_out2.json", "r", encoding="utf-8") as f:
    data = json.load(f) # nyni mam data ze souboru nactena


features =data["features"]
#features = features[0:20]
#UL, UR, DL, DR = quad_tree.quad_tree(features, 0)

#quad_tree.split_lines(features)

a_list = quad_tree.quad_tree(features)

#points_all = UL + UR + DL + DR

gj_structure = {"type": "FeatureCollection"}
gj_structure["features"] = a_list

# zapis souboru
with open("points_out3.json", "w", encoding="utf-8") as f:
    json.dump(gj_structure, f, indent=2, ensure_ascii=False) # index udela hezke odsazeni :-)

