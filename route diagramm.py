import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

def load_data(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) >= 4:  # Mindestens vier Teile müssen vorhanden sein
                numbers = [int(num) for num in parts[:-3]]  # Nur Zahlen, nicht Uhrzeit und Datum
                time = parse_time(parts[-2], parts[-3], parts[-1])  # Monat, Tag und Uhrzeit
                data.append((time, len(numbers)))
    return data

def parse_time(month_str, day_str, time_str):
    month = convert_month(month_str)  # Konvertiere Monat in Zahl
    day = int(day_str.strip())  # Tag als Zahl
    hour, minute, second = map(int, time_str.split('_'))  # Uhrzeit extrahieren
    return datetime(2024, month, day, hour, minute, second)

def convert_month(month_str):
    month_str = month_str.strip().lower()  # Entferne Leerzeichen und mache klein
    if month_str == 'mr':
        return 3
    elif month_str == 'apr':
        return 4
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
    plt.ylabel('Anzahl der Knoten')
    plt.title('Route Diagramm')
    plt.xticks(rotation=45)
    plt.xlim(times[0], times[-1])  # Setze die Grenzen der X-Achse
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))  # Ändere die Anzahl der X-Achsenticks
    plt.tight_layout()
    plt.savefig('diagramme/route_diagram.png', dpi=300)  # Speichere das Diagramm als PNG-Datei mit höherer Auflösung
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
    plt.ylabel('Anzahl der Knoten')
    plt.title('Erster Tag Diagramm (28. März)')
    plt.xticks(rotation=45)
    plt.xlim(times[0], times[-1])  # Setze die Grenzen der X-Achse
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))  # Ändere die Anzahl der X-Achsenticks
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Formatieren der Uhrzeit
    plt.tight_layout()
    plt.savefig(filename, dpi=300)  # Speichere das Diagramm als PNG-Datei mit höherer Auflösung
    plt.show()


filename = "tabellen/route-all.csv"
data = load_data(filename)
if data:
    plot_route_diagram(data)
    first_day_data = [entry for entry in data if entry[0].day == 28 and entry[0].month == 3]  # Filtere nach dem ersten Tag
    plot_firstroute_diagram(first_day_data, 'diagramme/first_day_diagram.png')  # Erstelle das Diagramm für den ersten Tag
else:
    print("Keine Daten zum Plotten gefunden.")
