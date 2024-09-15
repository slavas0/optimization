from datetime import datetime, time
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
graphfile = "tabellen/graph_neu.csv"
datafile = "tabellen/data-all.csv"
routefile = "tabellen/route-all.csv"
allroutesfile = "tabellen/unique-routes.csv"
graph= pd.read_csv(graphfile, header=None)
data_all = pd.read_csv(datafile)
indexfile = datafile

#Auswahl welche Datei benutzt werden soll für instanz_index Auswahl
def set_indexfile(newfile):
    global indexfile
    indexfile = newfile
#stundenzahl von deziaml in h:m format
def time_conv(dez):
    stunden = int(dez)
    dez = dez - stunden
    minuten = 0.1 * int(dez * 600)
    if  minuten < 10:
        mid = "h 0"
    else:
        mid = "h "
    return " " + str(stunden) + mid + f"{minuten:.1f}" + "m "
#Networkx DiGraph wird aus der Datei "graph.csv" erstellt
def create_graph():
    G = nx.DiGraph()
    for i in range(len(graph)):
        G.add_node(graph.iloc[i,2], pos=(graph.iloc[i,4], graph.iloc[i,5]))
        G.add_node(graph.iloc[i,3], pos=(graph.iloc[i,6], graph.iloc[i,7]))
        G.add_edge(graph.iloc[i,2], graph.iloc[i,3],name= graph.iloc[i,1]) #Gewichtung übergebenem Zeitpunkt
    return G

G=create_graph()
node_positions = nx.get_node_attributes(G, 'pos')
colors={}
#visualize route in graph
def viz_graph_route(Weg, beschreibung):
    plt.clf()
    Graph = graph_with_path(Weg)
    for j in G.nodes:
        colors[j] = "skyblue"
    colors[94] = "red"
    colors[162] = "red"
    for i in Weg:
        if i[0] == 94 or i[0] == 162:
            continue
        colors[i[0]] = "green"
    plt.title(beschreibung)
    nx.draw(Graph, pos=node_positions, with_labels=True, node_size=9, node_color=colors.values(), font_size=2.7)
    #plt.figure(figsize=(10, 6))  # Adjust figure size as needed
    plt.savefig("ergebnisse/graph " + beschreibung, dpi=400, bbox_inches='tight')
    #plt.show()
#Graph mit den gleichen Knoten wird erstellt, aber nur die Kanten des übergebenen Weges werden behalten
def graph_with_path(path):
    graph_path= nx.DiGraph()
    #G= create_graph()
    for node, data in G.nodes(data=True):
        graph_path.add_node(node, **data)
    for i in path:
        graph_path.add_edge(i[0],i[1])
    return graph_path
#konvertiert 'apr' '15' '00_02_03' in datetime format
def parse_time(month_str, day_str, time_str):
    month = convert_month(month_str)  # Konvertiere Monat in Zahl
    day = int(day_str.strip())  # Tag als Zahl
    time_str=str(time_str)

    hour, minute, second = map(int, time_str.split('_'))  # Uhrzeit extrahieren
    return datetime(2017, month, day, hour, minute, second)
#konvertiert Monat abkürzung in zahl
def convert_month(month_str):
    month_str = month_str.strip().lower()  # Entferne Leerzeichen und mache klein
    if month_str == 'mr':
        return 3
    elif month_str == 'apr':
        return 4
    elif month_str == 'mai':
        return 5
    else:
        raise ValueError(f"Ungültiger Monat: {month_str}")
#liste aller zeitstempel
def alldates():
    date_list = []
    for i in range(len(data_all)):

        converted_date = parse_time(data_all.iloc[i, -2], str(data_all.iloc[i, -3]), data_all.iloc[i, -1])

        date_list.append(converted_date)
        # if i==3211:
        if i == 4363:
            print(converted_date)
    return date_list
# Alle timestamps werden nach Wochentag in Listen eingeteilt in einem dict, keys sind 0 bis 6
def timestamp_weekdays():
    all_dates = alldates()                                    #0 ist Montag, 6 ist Sonntag etc.
    weekday_lists={0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
    for i in all_dates:
    #    if i.month==5:
    #        break
        weekday_lists[i.weekday()].append(i)           #datetime.weekday() gibt 0 bis 6 für Montag bis Sonntag zurück
    return weekday_lists
#nächsten 4 Methoden checken ob zeitpunkt t im Zeitslot liegt
def night_checker(t):                            # Diese Funktion prüfen ob der übergebene Zeitpunkt in einem bestimmten Intervall liegt
    time21= time(20,0)
    time3= time(2,0)
    if (time21 <= t.time()) or (t.time() <= time3):
        return True
    else:
        return False
def morning_checker(t):
    time3= time(6,0)
    time9= time(12,0)
    if time3 <= t.time() <= time9:
        return True
    else:
        return False
def afternoon_checker(t):
    time10= time(12,0)
    time16= time(18,0)
    if time10 <= t.time() <= time16:
        return True
    else:
        return False
def timeinbetween_checker(t):
    time9= time(2,0)
    time15= time(6,0)
    time10= time(18,0)
    time16= time(20,0)
    if time9 <= t.time() <= time15 or time10 <= t.time() <= time16:
        return True
    return False
#gibt die i-te zeile in dataroute zurück, zu testzwecken
def zeilerausgeben(i):
    j = 1
    with open(indexfile, 'r') as file:
        for line in file:
            if i <= j:
                return line
            else: j+=1
#gibt ein array mit (edge, edgelength) in miles zurück
def load_distance():
    edgelist = []
    earth_radius_km = 6371.01
    with open(graphfile, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            parts = [part for part in parts if part]
            numbers = [int(parts[1]), float(parts[4]), float(parts[5]), float(parts[6]), float(parts[7])]  # edgename, coord a, coord b
            latitude_a_rad = np.radians(numbers[2])
            latitude_b_rad = np.radians(numbers[4])
            longitude_a_rad = np.radians(numbers[1])
            longitude_b_rad = np.radians(numbers[3])
            delta_lat = latitude_b_rad - latitude_a_rad
            delta_lon = longitude_b_rad - longitude_a_rad
            a = np.sin(delta_lat / 2) * np.sin(delta_lat / 2) + \
                np.cos(latitude_a_rad) * np.cos(latitude_b_rad) * \
                np.sin(delta_lon / 2) * np.sin(delta_lon / 2)
            c = 2 * np.arcsin(np.sqrt(a))
            distance_km = earth_radius_km * c  # Distance in kilometers
            dist = distance_km * 0.621371  # Conversion factor to miles
            erg = [numbers[0], dist]
            edgelist.append(erg)
    return edgelist
#Performance vorteil durch globale variable
distance_tab = load_distance()
#berechnung der dauer einer route
def calc_dur(route_a, row):
    speeds = row[:-3]
    route = [int(num) for num in route_a]
    erg = 0
    speeds = [float(x) for x in speeds]
    for i in range(len(route)-1):
        edge = findedge(route[i], route[i + 1])
        index = findindex(edge)
        if edge == 0:
            return 0
        try:
            if speeds[index] <= 3 or speeds[index] > 120:
                edgeweight = finddist(edge) / 3
            else:
                edgeweight = finddist(edge) / speeds[index]
        except:
            if int(edge) <= 1307 and int(edge) >= 1309:
                print(f"Error calculating edge weight for edge {edge}")
            edgeweight = 0.022331018689856326                                #avg duration per edge
        erg += edgeweight
    return erg
#gibt für jede kante das kantengewicht zurück, bestehend aus der anzahl wie oft die kante in sim_routes vorkam
def sim_weights(sim_routes):
    weights={}
    for i in range(len(graph)):
        weights[(graph.iloc[i,2],graph.iloc[i,3])]=0
    for i in sim_routes:
        for j in sim_routes[i]:
            weights[j]+=1
    return weights
#gibt zu einer liste von zeitpunkten, die liste der routen aus route-all zu diesen zeitpunkten zurück
def sim_routes(sim_dates):
    routes={}
    for dates in sim_dates:
        sim_indx = find_line(dates)
        counter = 0
        with open(routefile, 'r') as file:
            for line in file:
               if counter == sim_indx:
                   parts = line.strip().split(',')
                   parts = [part for part in parts if part]
                   del parts[-3:]
                   sorted_path = [(int(parts[i]), int(parts[i + 1])) for i in range(len(parts) - 1)]
                   routes[dates] = sorted_path
                   break
               counter += 1
    return routes
#findet route zum datum
def find_route(date):
    with open(routefile, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            parts = [part for part in parts if part]
            #del parts[:-3]
            time = parts[-3:]
            time = parse_time(time[1], time[0], time[2])
            if date==time:
                del parts[-3:]
                return parts
    return None
#findet die Zeile aus data_all zu dem Datum "date"
def find_line(date):
  #  print("Start!!!")
    for i in range(len(data_all)):
        converted_date= parse_time(data_all.iloc[i,-2], str(data_all.iloc[i,-3]), data_all.iloc[i,-1])
        if date==converted_date:
          #  print("Ende!!!")
            return i
    return ValueError(f"no line found for {date}")
#finde index der kante zur edgename   (ungleicheit durch fehlende kanten in der nummerierung)
def findindex(edge):
    with open(datafile, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            parts = [part for part in parts if part]
            for i in range(len(parts)):
                if int(parts[i]) == edge:
                    return i
            break
    return 0
#finde edgename zu knoten a nach knoten b
def findedge(a, b):
    with open(graphfile, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            numbers = [int(num) for num in parts[:4]]
            if numbers[2] == a and numbers[3] == b:
                return numbers[1]
    print("Keine edge gefunden")
    return 0
def findnode(edge):
    with open(graphfile, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            numbers = [int(num) for num in parts[:4]]
            if numbers[1] == edge:
                return numbers[2], numbers[3]
    print(f"Keine edge gefunden für {edge}")
    return 0, 0
#findet im distance tab zur edge die länge der kante
def finddist(edge):
    for comb in distance_tab:
        if comb[0] == edge:
            return comb[1]
    print("Keine dist gefunden")
    return 0
#zu guter letzt die definition der regionen
def region(linie):
    alle = []
    alle = data_all.columns
    alle = [int(x) for x in alle[:-3]]
    #print(alle)
    #region1 = [94, 209, 210, 522, 344, 222, 223, 329, 305, 517, 354, 410, 198, 147, 146, 415, 122, 348, 170, 169, 279, 460, 306, 307, 166, 307, 166, 163, 164]
    #region1 = [989, 1006, 990, 1007, 991, 1008, 992, 1009, 993, 1010, 1011, 994, 670, 673, 672, 669, 668, 671]
    #oben links
    region1 = [] + list(range(989, 994)) + list(range(1006, 1011)) + list(range(668, 673))
    #unten
    region2 = list(range(1106, 1114)) + list(range(751, 756)) + [762, 763] + list(range(459, 461)) + list(range(473, 476)) + [263, 278] + list(range(818, 823)) + list(range(981, 988)) + list(range(1069, 1093)) + [1268, 1128, 1129, 1130, 1123, 1155, 1154, 1131, 1156, 1157, 1159] + list(range(1135, 1139)) + list(range(1119, 1124))
    #über innenstadt
    region3 = list(range(592, 601)) + [319, 298, 794, 793, 621, 622, 884, 877] + list(range(889, 897))
    #unter innenstadt
    region4 = [1181, 1178, 438, 980, 972, 1194] + list(range(604, 612)) + list(range(801, 806)) + list(range(812, 817)) + list(range(886, 888)) + list(range(578, 583))
    #innenstadt rechte hälfte
    region5 = [620, 925, 2011, 1297, 911, 1285, 2016, 2029, 1283, 1284, 2003, 2026, 2044, 956, 1296, 1295,
               1029, 2045, 2024, 2061, 2057, 2059, 2058, 1294, 1293, 1302, 656, 1292, 2060, 904, 2039, 2056,
               2040, 2018, 2019, 2040, 660, 918, 907, 657, 2050, 1269, 921, 908, 1038, 922, 2014, 2013, 2043,
               758, 2030, 863, 1282, 759, 1281, 958, 2038, 2012, 2037, 1031, 1056, 1280, 1279, 2000, 1174, 661,
               1278, 1277, 2032, 2031, 2046, 2055, 2060, 904, 2039, 244, 1276, 244, 584, 1303, 613, 586, 1175, 2001,
               615, 587, 1055, 616, 589, 1040, 618, 591, 959, 2025]
    #innenstadt linke hälfte
    region5b = [1297, 2026, 2044, 757, 1296, 1295, 1037, 2045, 2024, 2053, 2057, 2059, 1294, 1293, 659, 1305, 1292,
                2047, 1306, 243, 655, 1307, 658, 654, 2008, 1298, 2022, 2020, 2051, 2021, 1028, 1299, 871, 1036, 955,
                878, 872, 963, 1287, 879, 1288, 873, 954, 964, 1027, 1034, 1058, 1054, 1025, 1033, 1270, 1301, 1024, 1308,
                1309, 227, 865, 242, 2002, 681, 866, 2049, 2034, 2036, 2035, 2042, 680, 2009, 679, 926, 1289, 1259, 1290,
                1224, 953, 2048, 1223, 1258, 2006, 1275, 1222, 1257, 1271, 1300, 2033, 1304, 1221, 1256, 226, 1220, 241,
                1255, 1291, 933, 1272, 225, 1260, 880, 1219]
    #mitte unten
    region6 = list(range(182, 185)) + list(range(19, 26)) + list(range(59, 66)) + list(range(264, 278)) + list(range(1115, 1118)) + list(range(327, 334)) + list(range(368, 375)) + list(range(98, 101)) + list(range(133, 136)) + list(range(424, 430)) + list(range(463, 472)) + list(range(701, 705)) + list(range(682, 686)) + list(range(1196, 1203)) + list(range(1232, 1239)) + list(range(796, 800)) + list(range(807, 811)) + list(range(477, 490)) + [492, 1079, 1074, 456, 457, 458]
    #mitte, rechts von 94
    region7 = list(range(299, 309)) + list(range(279, 289)) + list(range(837, 848)) + list(range(856, 860)) + list(range(765, 771)) + list(range(1148, 1153)) + list(range(1167, 1172)) + list(range(824, 827)) + list(range(933, 946)) + list(range(926, 930)) + list(range(737, 739)) + list(range(623, 629)) + list(range(641, 653)) + list(range(1102, 1105)) + list(range(1098, 1101)) + list(range(531, 541)) + list(range(546, 556)) + list(range(1094, 1097)) + list(range(213, 225)) + list(range(229, 241)) + list(range(39, 53)) + list(range(79, 93)) + list(range(320, 326)) + list(range(196, 211)) + list(range(1045, 1052)) + list(range(949, 951)) + list(range(114, 122)) + list(range(149, 157)) + list(range(348, 359)) + list(range(389, 400))  + [1059, 1060, 1062, 1063, 1064, 772, 828, 844, 843, 168, 541, 850, 851, 852, 853, 854]   # -849 -855
    #unter innenstadt
    region8 = list(range(1240, 1255)) + list(range(1204, 1219)) + list(range(409, 414)) + list(range(419, 423)) + list(range(977, 980)) + list(range(968, 972)) + list(range(706, 719)) + list(range(687, 700)) + list(range(9, 11)) + list(range(179, 181)) + list(range(542, 544)) + list(range(898, 900)) + list(range(674, 677)) + [432, 433, 434, 436, 437, 438, 912, 913, 917, 903, 557, 560, 559, 1192, 1193, 506, 521, 1194, 1195, 455]
    #ganz oben
    region9 = [830, 846, 831, 847, 832, 848, 995, 1012, 996, 948, 1013, 523, 997, 527, 524, 1014, 1000, 1017, 1001,
               1186, 1183, 1185, 528, 525, 525, 529, 526, 932, 2005, 529, 526, 530, 530, 776, 785, 97, 777, 57, 96,
               56, 95, 55, 94, 54, 93, 744, 728, 53, 289, 727, 310, 290, 743, 311, 291, 312, 292, 786, 778, 787, 779,
               788, 780, 789, 408, 781, 367, 407, 366, 406, 406, 365, 365, 313, 293, 400, 359, 399, 358, 127, 162, 315,
               295, 128, 314, 294, 795, 1182, 1231, 1267, 318, 297, 317, 316, 296, 2027, 2010, 1189, 792, 791, 790, 782,
               1018, 1002, 1019, 1003, 1020, 1004, 1021, 1022, 1005, 163, 129, 164, 130, 165, 1188, 726, 745, 729, 746,
               730, 747, 731, 748, 999, 1016, 1015, 998, 783, 793, 794, 132, 1189, 404, 363]
    #rechts unter region9
    region9b = [125, 735, 736, 211, 212, 194, 195, 881, 874, 401, 402, 403, 362, 361, 360, 210, 193] + list(range(721, 726)) + list(range(740, 743)) + list(range(122, 127)) + list(range(157, 162)) + list(range(1224, 1231)) + list(range(1260, 1267))
    #unter der mittleren region
    region10 = [245, 764, 12, 246, 13, 247, 508, 248, 178, 496, 15, 249, 16, 250, 17,
                568, 636, 251, 511, 637, 569, 497, 638, 570, 639, 571, 640, 1125, 1132,
                567, 635, 566, 634, 565, 633, 564, 632, 563, 439, 415, 440, 416, 441, 27,
                417, 442, 418, 443, 449, 444, 450, 445, 512, 498, 169, 252, 77, 37, 76, 36,
                75, 35, 74, 34, 73, 513, 33, 72, 499, 170, 32, 71, 1, 31, 70, 30, 69, 29, 68,
                67, 28, 337, 378, 338, 379, 341, 174, 5, 382, 342, 383, 343, 384, 344,
                385, 345, 966, 386, 346, 517, 503, 387, 516, 501, 515, 514, 500, 4, 173, 3, 172,
                171, 2, 974, 967, 518, 504, 175, 6, 451, 446, 452, 447, 102, 453, 8, 177, 138, 104,
                137, 103, 139, 105, 140, 106, 176, 7, 141, 107, 142, 108, 143, 109, 144, 110, 975, 145,
                111, 146, 112, 519, 147, 836, 1141, 1160, 1142, 1161, 1143, 1162, 1144, 1163, 1145, 1164,
                14, 508, 493, 247, 494, 509, 510, 495, 376, 335, 340, 381, 377, 336, 339, 380, 973, 502, 972]
    regarray = [region1, region2, region3, region4, region5, region5b, region6, region7, region8, region9, region9b, region10]
    A = []
    for reg in range(len(regarray)):
        erg = 0
        for i in regarray[reg]:
            try:
                erg += linie[i]
            except:
                erg += 3
        #erg = erg * coef[reg]
        A.append(erg)
    return A