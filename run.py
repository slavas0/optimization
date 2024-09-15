import Schritte as schritt
import hilfsfunktionen as hf

#indexfile = "tabellen/test.csv"
indexfile = "tabellen/data-all.csv"
instance_time = hf.parse_time("Apr","08","14_01_19") #Samstag nachmittag 9-15Uhr  #zeit (False)
instanzindx = 4271                                                              #max 4363                   #zeile (True)
zeit_oder_zeile = True    #False = Zeitauswahl , True = Zeilenauswahl
#Gewichtungen:
weight_A = 1              #Geschwindigkeit
weight_B = 7              #Ähnlichkeit
num_elements = 20              #Anzahl Routen die in der Gr1 Gruppe als Ähnlichkeitsmaß gewählt werden (max 32)  25=~80%
coef = [0.2, 0.2, 1.0, 1.0, 0.5, 0.7,  0.4, 1.0, 1.1, 0.6, 0.6, 0.4]   #gewichtungen der Regionen 1 bis 10
#region: 1    2    3    4    5    5b    6    7    8    9    9b   10


#graph param7 a9 b11 steht für Parameter: Zeile 7, a=9, b=11
def solving(t, zeile):
    #intervals= schritt.nr1()
    A = schritt.nr2(t, coef)
    Gr = schritt.nr3(A)
    sim_list = schritt.nr4(Gr, num_elements)
    sim_routez = hf.sim_routes(sim_list)
    #test(sim_routez)
    sim_weightz = hf.sim_weights(sim_routez)
    return schritt.nr5(zeile, weight_A, weight_B, sim_weightz)
def instanz_erg(instanz_time, instanzindex, zeitoderzeile, schnell, algo, similar, route):
    instanz = hf.zeilerausgeben(instanzindex)
    thetime = str(instanz).strip().split(',')[-3:]
    thetime2 = hf.parse_time(thetime[1], thetime[0], thetime[2])
    with open(hf.datafile, 'r') as file:
        for line in file:
            if zeitoderzeile:
                break
            thetime3 = str(line).strip().split(',')[-3:]
            thetime4 = hf.parse_time(thetime3[1], thetime3[0], thetime3[2])
            if thetime4 == instanz_time:
                thetime2 = thetime4
                instanz = line
                break
    print(f"Die Zeit ist: {thetime2}")
    #routep = hf.find_route(thetime2)
    Kosten, Weg, shortp, samep = solving(thetime2, instanz)  # solving
    print(f"DER KÜRZESTE IST DAS: {shortp}")
    print(f"DAS ERGEBNIS IST DAS: {Weg}")
    print(f"DER ÄHNLICHSTE IST DAS: {samep}")
    #print(f"DIE ROUTE IST DAS: {routep}")
    derweg = [(Weg[i], Weg[i + 1]) for i in range(len(Weg) - 1)]
    shortestp = [(shortp[i], shortp[i + 1]) for i in range(len(shortp) - 1)]
    samestp = [(samep[i], samep[i + 1]) for i in range(len(samep) - 1)]
    #routestp = [(int(routep[i]), int(routep[i + 1])) for i in range(len(routep) - 1)]
    printweg = ""
    for p in Weg:
        printweg = printweg + str(p) + ","
    for t in range(len(thetime)):
        printweg += (thetime[t])
        if t < 2:
            printweg += ","
        else:
            printweg += "\n"
    with open('ergebnisse/routenergebnisse.csv', 'a') as file:
        file.write(printweg)
    # Print results and visualize routes
    print(f"Schnellste Route ist:     Dauer: {hf.time_conv(hf.calc_dur(shortp, str(instanz).strip().split(',')))}")
    if schnell:
        hf.viz_graph_route(shortestp, f"schnellste,  Zeile {instanzindex}, param-{instanzindex} a{weight_A} b{weight_B}")
    print(f"Algorithmus Lösung ist:   Dauer: {hf.time_conv(hf.calc_dur(Weg, str(instanz).strip().split(',')))}")
    if algo:
        hf.viz_graph_route(derweg, f"algorithmus,  Zeile {instanzindex}, param-{instanzindex} a{weight_A} b{weight_B}")
    print(f"Ähnlichste Route ist:     Dauer: {hf.time_conv(hf.calc_dur(samep, str(instanz).strip().split(',')))}")
    if similar:
        hf.viz_graph_route(samestp, f"ähnlichste,  Zeile {instanzindex}, param-{instanzindex} a{weight_A} b{weight_B}")
    #print(f"Route aus route-all ist:  Dauer: {hf.time_conv(hf.calc_dur(routep, str(instanz).strip().split(',')))}")
    if route:
        #hf.viz_graph_route(routestp, f"route-all,  Zeile {instanzindex}, param-{instanzindex} a{weight_A} b{weight_B}")
        pass
    return

#hier gibt es die Möglichkeit eine Reihe von Lösungen zu generieren -  kann ignoriert werden und nur die Parameter ganz oben benutzt werden wenn:
#instanzliste = [instanzindx] und instanz_erg(instance_time, i, zeit_oder_zeile, True, True, True, True) oder instanz_erg(instance_time, instanzindx, zeit_oder_zeile, True, True, True, True)
hf.set_indexfile(indexfile)
#instanzliste = [instanzindx]
instanzliste = list(range(4278, 4364))
for i in instanzliste:
    instanz_erg(instance_time, i, zeit_oder_zeile, False, True, False, False)

#Dauer: 5m45s für 5 Instanzen -> 11m40s für 10 Instanzen -> 1m10s pro Instanz
#Hardware 5800x, 16GB DDR4, braucht 4,5GHz Boosttakt und 4GB verfügbaren Arbeitspeicher
