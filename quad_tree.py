import turtle, statistics

def split_lines(json_file):
    # vypocet linii rezu
    body = []  # list souradnic
    for pnts in json_file:
        souradnice = pnts["geometry"]["coordinates"]
        x, y = souradnice
        body.append((x, y))


    body.sort(key=lambda p: p[0])  # serazeni podle x
    xmax = body[-1][0]
    xmin = body[0][0]

    body.sort(key=lambda p: p[1])  # serazeni podle y
    ymax = body[-1][1]
    ymin = body[0][1]

    x_mid = (xmax + xmin) / 2
    y_mid = (ymax + ymin) / 2
    return(x_mid, y_mid, xmax, xmin, ymax, ymin, body)




final_list = [] # seznam pro zapis finalnich prvku
a = [1,2] # seznam pro tvorbu id


def quad_tree(json_list, xmid, ymid, len_x, len_y, kvadrant = 0):
    # len -- delka odpovidajici pulce strany boundig boxu
    # mid -- delici hodnoty
    # kvadrant -- defaultne roven 0, meni se az po prvnim rozdeleni

    if len(json_list) < 50:
        a.sort(reverse=True)
        id = a[-1]# vytazeni id z id_seznamu
        # zapis id
        for i in json_list:
            i["properties"]["cluster_id"] = id
            final_list.append(i)
        a.pop() # vymazani last prvku
        a.append(id+2) # pridani prvku

        return (json_list)

    # vypocet linii rezu na zaklade kvadrantu
    if kvadrant ==1:
        xmid = xmid - len_x
        ymid = ymid + len_y

    elif kvadrant ==2:
        xmid = xmid + len_x
        ymid = ymid + len_y

    elif kvadrant ==3:
        xmid = xmid - len_x
        ymid = ymid - len_y

    elif kvadrant ==4:
        xmid = xmid + len_x
        ymid = ymid - len_y

    # seznamy pro 4 kvadranty bodu (D = down, U = up, R = right, L = left)
    UL = []
    UR = []
    DL = []
    DR = []

    # prochazim json_file a delim body do 4 kvadrantu -- vzniknou 4 dilci json soubory
    for pts in json_list:
        souradnice = pts["geometry"]["coordinates"]
        x, y = souradnice

        if x < xmid and y > ymid:
            UL.append(pts)
        elif x > xmid and y > ymid:
            UR.append(pts)
        elif x < xmid and y < ymid:
            DL.append(pts)
        else:
            DR.append(pts)

    # rekurzivne volam na 4 vznikle kvadranty
    quad_tree(UL,xmid, ymid,len_x/2, len_y/2, kvadrant=1)
    quad_tree(UR,xmid, ymid,len_x/2, len_y/2, kvadrant=2)
    quad_tree(DL,xmid, ymid,len_x/2, len_y/2, kvadrant=3)
    quad_tree(DR,xmid, ymid,len_x/2, len_y/2,kvadrant=4)

    return (final_list)


