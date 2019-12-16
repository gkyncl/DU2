import math, json, quad_tree, kresleni_zelva

# nacteni geoJSON souboru

with open("points_out2.json", "r", encoding="utf-8") as f:
    data = json.load(f) # nyni mam data ze souboru nactena


features =data["features"]


# vypocitej strany obdelnika:
xmid, ymid, xmax, xmin, ymax, ymin = quad_tree.split_lines(features)[0:6]
len_x = abs(xmax - xmin)/2
len_y = abs(ymax - ymin)/2


a_list = quad_tree.quad_tree(features, xmid, ymid, len_x, len_y)



# vytvoreni json vystupniho souboru
gj_structure = {"type": "FeatureCollection"}
gj_structure["features"] = a_list

# zapis souboru
with open("points_out3.json", "w", encoding="utf-8") as f:
    json.dump(gj_structure, f, indent=2, ensure_ascii=False) # index udela hezke odsazeni :-)

