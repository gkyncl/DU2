

def split_lines(feature_list):
    """
    Vypocita hodnoty pro prvni geometricke rozdeleni dat
    :param feature_list -- seznam jednotlivych bodu
    :return:
    xmid -- delici hodnota na ose x
    ymid -- delici hodnota na ose y
    bounding box:
    xmax -- maximalni x souradnice vstupnich bodu
    xmin -- minimalni x souradnice vstupnich bodu
    ymax -- maximalni y souradnice vstupnich bodu
    ymin -- minimalni y souradnice vstupnich bodu

    """
    body = []  # seznam pro ukladani souradnic

    # prochazeni bodu a ukladni jejich souradnic do seznamu pro dalsi vypocet
    for pnt in feature_list:
        souradnice = pnt["geometry"]["coordinates"]
        body.append(souradnice)

    # inicializace promennych na souradnice prvniho bodu ze seznamu souradnic
    xmax = body[0][0]
    xmin = body[0][0]
    ymax = body[0][1]
    ymin = body[0][1]

    # prochazeni souradnic a hledani maximalnich a minimalnich hodnot
    for pt in body:
        x = pt[0]
        y = pt[1]
        if x > xmax:
            xmax = x
        elif x < xmin:
            xmin = x
        if y > ymax:
            ymax = y
        elif y < ymin:
            ymin = y

    # vypocet geometrickych stredu v x a y smeru
    x_mid = (xmax + xmin) / 2
    y_mid = (ymax + ymin) / 2
    return(x_mid, y_mid, xmax, xmin, ymax, ymin)


def quad_tree(json_list, xmid, ymid, len_x, len_y, aid_store, final_list, kvadrant = 0,):
    """
    funkce na deleni bodu dle quad tree algoritmu
    :param json_list -- vstupni bodova data vznikla z geoJSON souboru
    :param xmid -- delici hodnota na x ose, dle ktere byly body rozdeleny
    :param ymid -- delici hodnota na y ose, dle ktere byly body rozdeleny
    :param len_x -- delka odpovidajici pulce strany obdelniku ve smeru osy x, ktery funkce v danou chvili zpracovava
    :param len_y -- delka odpovidajici pulce strany obdelniku ve smeru osy y, ktery funkce v danou chvili zpracovava
    :param aid_store -- jednoprvkovy seznam k zapisu cluster_id
    :param final_list -- seznam k zapisu vyslednych bodu s atributem cluster_id
    :param kvadrant -- oznaceni pocitaneho kvadrantu (defaultne rovno 0 -- meni se po prvnim rozdeleni bodu)
    :return:
    final_list -- vystupni seznam bodu s pridanym atributem cluster_id
    json_list -- cast seznamu bodu, ktery funkce v danou chvili pocita -- slouzi jen pro predavani mezi vnorenymi funkcemi
    aid_store -- jednoprvkovy seznam uchovavajici vzdy aktualni cluster_id
    """

    # testovani velikosti vstupniho souboru, pokud splnuje podminku, je bodum zapsano cluster_id
    if len(json_list) < 50:
        aid = aid_store[0] # vytazeni id z id seznamu
        for i in json_list:
            i["properties"]["cluster_id"] = aid
            final_list.append(i)
        aid_store.pop() # vymazani posledniho (jedineho) prvku
        aid_store.append(aid+1) # pridani prvku o 1 vetsi nez byl puvodni prvek

        return (final_list, json_list, aid_store)

    # vypocet linii rezu na zaklade kvadrantu

    # levy horni kvadrant
    if kvadrant == 1:
        xmid = xmid - len_x
        ymid = ymid + len_y

    # pravy horni kvadrant
    elif kvadrant == 2:
        xmid = xmid + len_x
        ymid = ymid + len_y

    # levy spodni kvadrant
    elif kvadrant == 3:
        xmid = xmid - len_x
        ymid = ymid - len_y

    # pravy spodni kvadrant
    elif kvadrant == 4:
        xmid = xmid + len_x
        ymid = ymid - len_y

    # seznamy pro 4 kvadranty bodu (L = lower, U = upper, R = right, L = left)
    UL = []
    UR = []
    LL = []
    LR = []

    # prochazi se seznam bodu a je delen do 4 kvadrantu -- vzniknou 4 dilci seznamy bodu
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

    # rekurzivni volani funkce na 4 vznikle kvadranty
    quad_tree(UL,xmid, ymid, len_x/2, len_y/2, aid_store, final_list, kvadrant=1)
    quad_tree(UR,xmid, ymid, len_x/2, len_y/2, aid_store, final_list, kvadrant=2)
    quad_tree(LL,xmid, ymid, len_x/2, len_y/2, aid_store, final_list, kvadrant=3)
    quad_tree(LR,xmid, ymid, len_x/2, len_y/2, aid_store, final_list, kvadrant=4)

    return (final_list, json_list, aid_store)


