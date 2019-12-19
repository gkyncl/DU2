import turtle, statistics

def split_lines(feature_list):
    # vypocet linii rezu
    body = []  # list souradnic
    for pnt in feature_list:
        souradnice = pnt["geometry"]["coordinates"]
        body.append(souradnice)


    body.sort(key=lambda p: p[0])  # serazeni podle x
    xmax = body[-1][0]
    xmin = body[0][0]

    body.sort(key=lambda p: p[1])  # serazeni podle y
    ymax = body[-1][1]
    ymin = body[0][1]

    x_mid = (xmax + xmin) / 2
    y_mid = (ymax + ymin) / 2
    return(x_mid, y_mid, xmax, xmin, ymax, ymin, body)


def quad_tree(json_list, xmid, ymid, len_x, len_y, aid_store, final_list, kvadrant = 0,):
    # len -- delka odpovidajici pulce strany obdelniku, ktery funkce v danou chvili zpracovava
    # mid -- delici hodnoty obdelniku o uroven vys
    # aid_maker -- jednoprvkovy seznam k zapisu cluster_id
    # kvadrant -- defaultne roven 0, meni se az po prvnim rozdeleni
    print(len(json_list))
    print(aid_store)
    if len(json_list) < 50:
        aid = aid_store[0] # vytazeni id z id_seznamu
        for i in json_list:
            i["properties"]["cluster_id"] = aid
            final_list.append(i)
        aid_store.pop() # vymazani posledniho (jedineho) prvku
        aid_store.append(aid+1) # pridani prvku o 1 vetsi nez byl puvodni prvek

        return (final_list, json_list, aid_store)

    # vypocet linii rezu na zaklade kvadrantu
    if kvadrant == 1:
        xmid = xmid - len_x
        ymid = ymid + len_y

    elif kvadrant == 2:
        xmid = xmid + len_x
        ymid = ymid + len_y

    elif kvadrant == 3:
        xmid = xmid - len_x
        ymid = ymid - len_y

    elif kvadrant == 4:
        xmid = xmid + len_x
        ymid = ymid - len_y

    # seznamy pro 4 kvadranty bodu (L = lower, U = upper, R = right, L = left)
    UL = []
    UR = []
    LL = []
    LR = []

    # prochazim json_file a delim body do 4 kvadrantu -- vzniknou 4 dilci json soubory
    for pt in json_list:
        souradnice = pt["geometry"]["coordinates"]
        x, y = souradnice

        if x < xmid and y > ymid:
            UL.append(pt)
        elif x > xmid and y > ymid:
            UR.append(pt)
        elif x < xmid and y < ymid:
            LL.append(pt)
        else:
            LR.append(pt)

    # rekurzivne volam na 4 vznikle kvadranty
    quad_tree(UL,xmid, ymid, len_x/2, len_y/2, aid_store, final_list, kvadrant=1)
    quad_tree(UR,xmid, ymid, len_x/2, len_y/2, aid_store, final_list, kvadrant=2)
    quad_tree(LL,xmid, ymid, len_x/2, len_y/2, aid_store, final_list, kvadrant=3)
    quad_tree(LR,xmid, ymid, len_x/2, len_y/2, aid_store, final_list, kvadrant=4)

    return (final_list, json_list, aid_store)


