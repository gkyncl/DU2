import turtle

def split_lines(json_file):
    # vypocita linie rezu
    #features = json_file["features"][0:30]
    body = []  # list souradnic
    for pnts in json_file:
        souradnice = pnts["geometry"]["coordinates"]
        x, y = souradnice
        body.append((x, y))


    body.sort(key=lambda p: p[0])  # serazeni podle x
    Xmax = body[-1][0]
    Xmin = body[0][0]

    body.sort(key=lambda p: p[1])  # serazeni podle y
    Ymax = body[-1][1]
    Ymin = body[0][1]

    #drawing(body, Xmax, Ymax)

    X_mid = (Xmax + Xmin) / 2
    Y_mid = (Ymax + Ymin) / 2
    return(X_mid, Y_mid, Xmax, Xmin, Ymax, Ymin)

def drawing(body_all, xmax, ymax):
    for pts in body_all:
        turtle.Screen().setup(600 + 4, 400 + 8)  # fudge factors due to window borders & title bar
        turtle.Screen().setworldcoordinates(0, 0, 400, 600)

        turtle.penup()
        turtle.goto(pts)
        turtle.pendown()
        turtle.dot(5, "blue")
    turtle.exitonclick()




final_list = [] # seznam pro zapis finalnich prvku
a = [1,2] # seznam pro tvorbu id


def quad_tree(json_list, kvadrant = 0, x_max = 0, x_min = 0, y_max = 0, y_min = 0):
    print("delka:", len(json_list))

    if len(json_list) < 8:
        #id = id + 1
        #id = random.randint(0,200)
        a.sort(reverse=True)
        Id = a[-1]# vytazeni id z id_seznamu
        for i in json_list:
            i["properties"]["cluster_id"] = Id
            final_list.append(i)
        a.pop() # vymazani last prvku
        a.append(Id+2) # pridani prvku

        return (json_list) # navrat

    if kvadrant ==0:
        X_mid, Y_mid = split_lines(json_list)[0:2]
    elif kvadrant ==1:
        X_mid = (x_min + x_max)/2
        Y_mid = (y_min + y_max)/2
    elif kvadrant ==2:
        X_mid = (x_min + x_max) / 2
        Y_mid = (y_min + y_max) / 2
    elif kvadrant ==3:
        X_mid = (x_min + x_max) / 2
        Y_mid = (y_min + y_max) / 2
    elif kvadrant ==4:
        X_mid = (x_min + x_max) / 2
        Y_mid = (y_min + y_max) / 2


    UL = [] # seznamy pro 4 kvadranty bodu (D = down, U = up, R = right, L = left)
    UR = []
    DL = []
    DR = []

    # prochazim json_file a delim body do 4 kvadrantu - vzniknou 4 dilci json soubory
    for pts in json_list:
        souradnice = pts["geometry"]["coordinates"]
        x, y = souradnice


        if x < X_mid and y > Y_mid:
            UL.append(pts)
        elif x > X_mid and y > Y_mid:
            UR.append(pts)
        elif x < X_mid and y < Y_mid:
            DL.append(pts)
        else:
            DR.append(pts)

    print("UL:", UL)
    print("UR:", UR)
    print("DL:", DL)
    print("DR:", DR)

    Xmax, Xmin, Ymax, Ymin = split_lines(json_list)[2:6]

    # rekurzivne volam na 4 vznikle kvadranty
    quad_tree(UL, kvadrant=1, x_max=X_mid, x_min=Xmin, y_max=Ymax, y_min=Y_mid)
    quad_tree(UR, kvadrant=2, x_max=Xmax, x_min=X_mid, y_max=Ymax, y_min=Y_mid)
    quad_tree(DL, kvadrant=3, x_max=X_mid, x_min=Xmin, y_max=Y_mid, y_min=Ymin)
    quad_tree(DR, kvadrant=4, x_max=Xmax, x_min=X_mid, y_max=Y_mid, y_min=Ymin)



    return (final_list)


