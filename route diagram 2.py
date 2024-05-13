#route diagram 2 erzeugt die selbe grafik wie route diagram (1) nur die amplitude gibt die tatsächliche zeit an, nicht nur knotenzahl (route von 94 nach 162)
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np

def addnum(speeds, routes):
    erg = 0
    distance_tab = load_distance()
    for i in range(len(routes)-1):
        edge = findedge(routes[i], routes[i + 1])
        index = findindex(edge)
        #print(edge, index)
        if edge == 0:
            return 0
       # print(len(speeds))
        try:
            if speeds[index] == 0:
                return 10
            edgeweight = finddist(distance_tab, edge) / speeds[index]
       #     print(f"erfolgreich für {edge}")
        except:
            print(f"Error calculating edge weight for edge {edge}")
            return None
        erg += edgeweight
    return erg
def findindex(edge):
    filename5 = "tabellen/data-all.csv"
    with open(filename5, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            parts = [part for part in parts if part]
            for i in range(len(parts)):
                if int(parts[i]) == edge:
                    return i
            break
    return 0
def findedge(a, b):
    filename4 = "tabellen/graph.csv"
    with open(filename4, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            numbers = [int(num) for num in parts[:4]]  # Nur Zahlen, nicht Uhrzeit und Datum
            if numbers[2] == a and numbers[3] == b:
                return numbers[1]
    print("Keine edge gefunden")
    return 0
def finddist(arr, edge):
    for comb in arr:
        if comb[0] == edge:
            return comb[1]
    print("Keine dist gefunden")
    return 0
def load_distance():
    filename3 = "tabellen/graph.csv"
    data3 = []
    earth_radius_km = 6371.01
    with open(filename3, 'r') as file:
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
            data3.append(erg)
    return data3
def load_speedsroute():
    filename2 = "tabellen/data-all.csv"
    data2 = []
    with open(filename2, 'r') as file:
        start = True
        for line in file:
            if start:
                start = False
                continue
            #print(line)
            parts = line.strip().split(',')
            parts = [part for part in parts if part]
            #print(len(parts))
            numbers = [float(num) for num in parts[:-3]]  #
            #time = parse_time(parts[-2], parts[-3], parts[-1])  # Monat, Tag und Uhrzeit
            data2.append(numbers)
            #print(len(numbers))
    return data2
def load_dataroute():
    filename1 = "tabellen/route-all.csv"
    data = []
    speeds = load_speedsroute()
    with open(filename1, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            parts = [part for part in parts if part]
            if len(parts) >= 4:  # Mindestens vier Teile müssen vorhanden sein
                numbers = [int(num) for num in parts[:-3]]  # Nur Zahlen, nicht Uhrzeit und Datum
                time = parse_time(parts[-2], parts[-3], parts[-1])  # Tag, Monat und Uhrzeit
                lenroute = addnum(speeds[len(data)], numbers)
                data.append((time, lenroute))
                print(time)
    return data

def parse_time(month_str, day_str, time_str):
    month = convert_month(month_str)  # Konvertiere Monat in Zahl
    day = int(day_str.strip())  # Tag als Zahl
    hour, minute, second = map(int, time_str.split('_'))  # Uhrzeit extrahieren
    return datetime(2018, month, day, hour, minute, second)

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

def calculate_color(hour, minute):
    total_minutes = hour * 60 + minute
    normalized_minutes = total_minutes / (24 * 60)  # Normalisierte Minuten von 0 bis 1
    # Definiere die Farbpalette von Mitternacht (dunkelblau) bis kurz vor Mitternacht (gelb)
    color = (normalized_minutes, 0.5, 1 - normalized_minutes)  # RGB-Farben
    return color

def plot_route_diagram(data):
    times, values = zip(*data)
    plt.figure(figsize=(12, 6))  # Ändere die Größe des Diagramms
    for i in range(len(times) - 1):
        x = [times[i], times[i + 1]]
        y = [values[i], values[i + 1]]
        hour, minute = times[i].hour, times[i].minute
        color = calculate_color(hour, minute)
        plt.fill_between(x, y, color=color, alpha=0.5, linewidth=0)
    plt.plot(times, values, color='green')
    plt.xlabel('Datum')
    plt.ylabel('Zeit von 94 nach 162')
    plt.title('Route Diagramm')
    plt.xticks(rotation=45)
    plt.xlim(times[0], times[-1])  # Setze die Grenzen der X-Achse
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))  # Ändere die Anzahl der X-Achsenticks
    plt.tight_layout()
    plt.savefig('diagramme/route_diagram2.png', dpi=300)  # Speichere das Diagramm als PNG-Datei mit höherer Auflösung
    plt.show()

def plot_firstroute_diagram(data, filename):
    times, values = zip(*data)
    plt.figure(figsize=(12, 6))  # Ändere die Größe des Diagramms
    for i in range(len(times) - 1):
        x = [times[i], times[i + 1]]
        y = [values[i], values[i + 1]]
        hour, minute = times[i].hour, times[i].minute
        color = calculate_color(hour, minute)
        plt.fill_between(x, y, color=color, alpha=0.5, linewidth=0)
    plt.plot(times, values, color='green')
    plt.xlabel('Uhrzeit')  # Ändere die Beschriftung der X-Achse
    plt.ylabel('Zeit von 94 nach 162')
    plt.title('Erster Tag Diagramm2 (28. März)')
    plt.xticks(rotation=45)
    plt.xlim(times[0], times[-1])  # Setze die Grenzen der X-Achse
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))  # Ändere die Anzahl der X-Achsenticks
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Formatieren der Uhrzeit
    plt.tight_layout()
    plt.savefig(filename, dpi=300)  # Speichere das Diagramm als PNG-Datei mit höherer Auflösung
    plt.show()


data = load_dataroute()

if data:
    plot_route_diagram(data)
    first_day_data = [entry for entry in data if entry[0].day == 28 and entry[0].month == 3]  # Filtere nach dem ersten Tag
    plot_firstroute_diagram(first_day_data, 'diagramme/first_day_diagram.png')  # Erstelle das Diagramm für den ersten Tag
else:
    print("Keine Daten zum Plotten gefunden.")
