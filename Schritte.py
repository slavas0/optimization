import csv
import random
import hilfsfunktionen as hf
data_all = hf.data_all

def nr1():                                                                  #erstellt dict, das alle Daten von März und April (und Mai) nach Wochentag und Uhrzeit aufteilt
    weekday_lists=hf.timestamp_weekdays()
    intervals= {0: {"n":[], "m":[], "a":[], "i":[] },
                1: {"n":[], "m":[], "a":[], "i":[] },
                2: {"n":[], "m":[], "a":[], "i":[] },
                3: {"n":[], "m":[], "a":[], "i":[] },
                4: {"n":[], "m":[], "a":[], "i":[] },
                5: {"n":[], "m":[], "a":[], "i":[] },
                6: {"n":[], "m":[], "a":[], "i":[] }}
    for i in weekday_lists:
        for t in weekday_lists[i]:
            if hf.night_checker(t):
                intervals[i]["n"].append(t)
            elif hf.morning_checker(t):
                intervals[i]["m"].append(t)
            elif hf.afternoon_checker(t):
                intervals[i]["a"].append(t)
            elif hf.timeinbetween_checker(t):
                intervals[i]["i"].append(t)
    return intervals
def nr2(t, coef):                                                           #erstellt ein dict A, mit den Zeitpunkten als key und den Ähnlichkeitswert A(k) als value
    intervals= nr1()
    group_k=None
    if hf.night_checker(t):
        group_k=intervals[t.weekday()]["n"]
    if hf.morning_checker(t):
        group_k=intervals[t.weekday()]["m"]
    if hf.afternoon_checker(t):
        group_k=intervals[t.weekday()]["a"]
    if hf.timeinbetween_checker(t):
        group_k=intervals[t.weekday()]["i"]
    A={}
    linenumber_of_t=hf.find_line(t)
    for k in group_k:
        if k==t:
            continue
        linenumber_of_k= hf.find_line(k)
        line_of_k = {}
        for j in data_all.columns:
            if j == "Unnamed: 1045":
                break
            h = int(j)
            line_of_k[h] = data_all[j][linenumber_of_k]
        line_of_t = {}
        for m in data_all.columns:
            if m == "Unnamed: 1045":
                break
            h = int(m)
            line_of_t[h] = data_all[m][linenumber_of_t]
        werte1 = hf.region(line_of_k)
        werte2 = hf.region(line_of_t)
        diff = [a / b for a, b in zip(werte1, werte2)]
        prio = [diff[i]*coef[i] for i in range(12)]
        avg = sum(prio) / sum(coef)
        A[k] = abs(avg-1)
    return A
def nr3(dict_A):
    sorted_dates= sorted(dict_A, key= dict_A.get)
    length_group = int(len(dict_A)/5)
    Gr={}
    for j in range(5):
        group_list=[]
        for i in range(length_group):
            group_list.append(sorted_dates[j*length_group+i])
        Gr[j+1]=group_list
    return Gr
def nr4(dict_Gr_i, num_elements1):
    sim_list=[]
    for i in dict_Gr_i:
        counter = 0
        random.shuffle(dict_Gr_i[i])
        for j in dict_Gr_i[i]:
            if counter < num_elements1:
                #print(counter)
                #viz.viz_routeall_path(j)
                sim_list.append(j)
                counter+=1
                continue
            break
        break
        num_elements1 = int(num_elements1/2)
    #viz.viz_routeall_pathz(sim_list)
    return sim_list
def nr5(zeile, a, b, sim_wei):
    with open(hf.allroutesfile, 'r') as csvfile:
        reader = csv.reader(csvfile)
        unique_routes = []
        c = 0
        for line in reader:
            c+=1
            elem = [int(x) for x in line]
            unique_routes.append(elem)
            if c > 1300:   #nur die ersten x von ca 1300 routen
                break
        row = str(zeile).strip().split(',')[:-3]
        best = []
        f1werte = []
        f2werte = []
        y = 0
        for route in unique_routes:
            y+=1
            if y%30 == 0:
                print(f"{(y/12.7):.2f}%")  # formats the result to 2 decimal places
            f2 = 0
            for i in range(len(route)-1):
                f2 += sim_wei[int(route[i]), int(route[i+1])]
            f1 = hf.calc_dur(route, row)
            f1werte.append(f1)
            f2werte.append(f2)
            best.append(route)
        f1norm = [int(1000*float((x-min(f1werte)+0.1)/(max(f1werte)-min(f1werte)+0.2))) for x in f1werte]
        f2norm = [int(1000*float((x-min(f2werte)+0.1)/(max(f2werte)-min(f2werte)+0.2))) for x in f2werte]
        besteserg = a * f1norm[0] - b * f2norm[0]
        besterindx = 0
        kuerzesterindx = 0
        aehnlichsterindx = 0
        for i in range(len(best)):
            if i == 0:
                continue
            erg = a * f1norm[i] - b * f2norm[i]
            if f1norm[i] < f1norm[kuerzesterindx]:
                kuerzesterindx = i
            if f2norm[i] < f2norm[kuerzesterindx]:
                aehnlichsterindx = i
            if erg <= besteserg:
                besteserg = erg
                besterindx = i
                #print(f"besseres resultat: {besteserg, besterindx}")
        print(f"endresultat: a*opt-b*sim={besteserg}, aus opt={f1norm[besterindx]/10}%, sim={f2norm[besterindx]/10}%")
    return besteserg, best[besterindx], best[kuerzesterindx], best[aehnlichsterindx]