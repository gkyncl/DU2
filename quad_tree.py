import turtle, statistics

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


    #drawing(body, Xmax, Xmin, Ymax, Ymin)

    X_mid = (Xmax + Xmin) / 2
    Y_mid = (Ymax + Ymin) / 2
    return(X_mid, Y_mid, Xmax, Xmin, Ymax, Ymin, body)

def drawing(body_all, xmax, xmin, ymax, ymin, body):
    # vykresleni vstupnich bodu
    r = []
    l = []
    for pts in body_all:
        r.append(pts[0])
        l.append(pts[1])
    # preskalovani souradnic pomoci z-skoru
    mean_x = statistics.mean(r)
    sd_x = statistics.stdev(r)

    mean_y = statistics.mean(l)
    sd_y = statistics.stdev(l)

    for pt in body_all:
        x = 200*((pt[0]-mean_x)/sd_x)
        y = 200*((pt[1]-mean_y)/sd_y)
        turtle.speed(50)
        turtle.penup()
        turtle.goto(x,y)
        turtle.pendown()
        turtle.dot(5, "blue")

    first = []
    second = []
    #third = []
    #fourth = []
    for values in body:
        # rozdeleni na 4 seznamy
        first.append(values[0])
        second.append(values[1])
        #third.append(values[2])
        #fourth.append(values[3])

    # preskalovani souradnic pomoci z-skoru
    mean_first = statistics.mean(first)
    sd_first = statistics.stdev(first)

    mean_second = statistics.mean(second)
    sd_second = statistics.stdev(second)

    #mean_third = statistics.mean(third)
    #sd_third = statistics.stdev(third)

    #mean_fourth = statistics.mean(fourth)
    #sd_fourth = statistics.stdev(fourth)

    for vals in body:
        x1 = 200 * ((vals[0] - mean_first) / sd_first)
        y1 = 200 * ((vals[1] - mean_second) / sd_second)

        #x2 = 200 * ((vals[0] - mean_first) / sd_first)
        #y2 = 200 * ((vals[3] - mean_fourth) / sd_fourth)

        #x3 = 200 * ((vals[2] - mean_third) / sd_third)
        #y3 = 200 * ((vals[2] - mean_third) / sd_third)

        #x4 = 200 * ((vals[2] - mean_third) / sd_third)
        #y4 = 200 * ((vals[3] - mean_fourth) / sd_fourth)

        turtle.speed(50)
        turtle.penup()
        turtle.goto(x1, y1)
        turtle.pendown()
        turtle.dot(5, "red")
        #turtle.penup()
        #turtle.goto(x2, y2)
        #turtle.pendown()
        #turtle.dot(5, "red")
        #turtle.penup()
        #turtle.goto(x3, y3)
        #turtle.pendown()
        #turtle.dot(5, "red")
        #turtle.penup()
        #turtle.goto(x4, y4)
        #turtle.pendown()
        #turtle.dot(5, "red")

    turtle.exitonclick()






final_list = [] # seznam pro zapis finalnich prvku
points_kresleni = []
a = [1,2] # seznam pro tvorbu id


def quad_tree(json_list, xmid, ymid, len_x, len_y, kvadrant = 0):
    print("delka:", len(json_list))
    # len -- delka strany boundig boxu
    # mid -- delici hodnoty

    if len(json_list) < 5:
        a.sort(reverse=True)
        Id = a[-1]# vytazeni id z id_seznamu
        for i in json_list:
            i["properties"]["cluster_id"] = Id
            final_list.append(i)
        a.pop() # vymazani last prvku
        a.append(Id+2) # pridani prvku
        #print("deleni:",x_max, x_min, y_max, y_min)


        return (json_list) # navrat

    # vypocet linii rezu na zaklade kvadrantu
    if kvadrant ==0:
        X_mid, Y_mid = xmid, ymid
        #Xmax, Xmin, Ymax, Ymin = split_lines(json_list)[2:6] # kraje puvodniho bounding boxu
        print("0")
    elif kvadrant ==1:
        xmid = xmid - len_x
        ymid = ymid + len_y

        print("1")
    elif kvadrant ==2:
        xmid = xmid + len_x
        ymid = ymid + len_y
        print("2")
    elif kvadrant ==3:
        xmid = xmid - len_x
        ymid = ymid - len_y
        print("3")
    elif kvadrant ==4:
        xmid = xmid + len_x
        ymid = ymid - len_y
        print("4")



    UL = [] # seznamy pro 4 kvadranty bodu (D = down, U = up, R = right, L = left)
    UR = []
    DL = []
    DR = []

    # prochazim json_file a delim body do 4 kvadrantu - vzniknou 4 dilci json soubory
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

    print("UL:", UL)
    print("UR:", UR)
    print("DL:", DL)
    print("DR:", DR)



    # rekurzivne volam na 4 vznikle kvadranty
    quad_tree(UL,xmid, ymid,len_x/4, len_y/4, kvadrant=1)
    quad_tree(UR,xmid, ymid,len_x/4, len_y/4, kvadrant=2, )
    quad_tree(DL,xmid, ymid,len_x/4, len_y/4, kvadrant=3, )
    quad_tree(DR,xmid, ymid,len_x/4, len_y/4,kvadrant=4, )



    return (final_list, points_kresleni)


def cut_lines_draw(body):
    first = []
    second = []
    third = []
    fourth = []
    for values in body:
        # rozdeleni na 4 seznamy
        first.append(values[0])
        second.append(values[1])
        third.append(values[2])
        fourth.append(values[3])

    # preskalovani souradnic pomoci z-skoru
    mean_first = statistics.mean(first)
    sd_first = statistics.stdev(first)

    mean_second = statistics.mean(second)
    sd_second = statistics.stdev(second)

    mean_third = statistics.mean(third)
    sd_third = statistics.stdev(third)

    mean_fourth = statistics.mean(fourth)
    sd_fourth = statistics.stdev(fourth)

    for vals in body:
        x1 = 200*((vals[0]-mean_first)/sd_first)
        y1 = 200*((vals[2]-mean_third)/sd_third)

        x2 = 200*((vals[0]-mean_first)/sd_first)
        y2 = 200*((vals[3]-mean_fourth)/sd_fourth)

        x3 = 200*((vals[2]-mean_third)/sd_third)
        y3 = 200*((vals[2]-mean_third)/sd_third)

        x4 = 200*((vals[2]-mean_third)/sd_third)
        y4 = 200*((vals[3]-mean_fourth)/sd_fourth)

        turtle.speed(50)
        turtle.penup()
        turtle.goto(x1, y1)
        turtle.pendown()
        turtle.dot(5, "blue")
        turtle.penup()
        turtle.goto(x2, y2)
        turtle.pendown()
        turtle.dot(5, "blue")
        turtle.penup()
        turtle.goto(x3, y3)
        turtle.pendown()
        turtle.dot(5, "blue")
        turtle.penup()
        turtle.goto(x4, y4)
        turtle.pendown()
        turtle.dot(5, "blue")

        turtle.bye()
