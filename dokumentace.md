# Dělení adresních bodů

Program načte vstupní data `input.geojson` a pomocí algoritmu **quadtree** je dělí do skupin. Dělení probíhá tak dlouho, dokud není počet prvků ve všech skupinách menší než 50. Každému bodu je následně přidán atribut `cluster_id`, který je jedinečný pro každou skupinu bodů a popisuje příslušnost bodu k dané skupině. Výsledný soubor je zapsán a uložen jako `output.geojson`. 

#### Vstupy a výstupy

Vstupem je geoJSON soubor - feature collection bodů (`input.geojson`). Výstupem je taktéž geoJSON soubor (`output.geojson`), ve kterém jsou zachovány všechny jeho vstupní atributy a navíc je přidán atribut `cluster_id`.

#### Jak program pracuje

Program `split.py` načte vstupní data. Rozbalí geoJSON soubor a předává ho dál. 

Na rozbalený geoJSON soubor je z modulu `quad_tree.py` volána funkce `split_lines`, která vypočítá souřadnice bounding boxu kolem vstupních dat a dělící hodnoty sloužící k následnému dělení bodů. 

Dále je na vstupní data zavolána funkce `quad_tree` z modulu `quad_tree.py`, která na základě dělících hodnot a hodnot odpovídajícím polovinám délky stran bounding boxu dělí body do 4 segmentů, na které je následně funkce rekurzivně volána znovu, dokud není splněna podmínka o počtu prvků ve skupině. 

Parametry jednotlivých funkcí jsou popsány v rámci zdrojového kódu.



