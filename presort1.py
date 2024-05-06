import csv

def count_numbers_in_row(row):
    count = 0
    for item in row:
        try:
            float(item)  # Versuche, das Element in eine Zahl umzuwandeln
            count += 1
        except ValueError:
            pass  # Wenn das Element keine Zahl ist, überspringe es
    return count

def count_row_length(filename):
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        row_lengths = []
        for row in reader:
            numbers_count = count_numbers_in_row(row)
            row_lengths.append((numbers_count, row))  # Tupel (Anzahl der Zahlen, Zeile) hinzufügen
    return row_lengths

def write_sorted_rows(sorted_rows, output_filename):
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for count, row in sorted_rows:
            writer.writerow(row)

# Beispielaufruf
filename = 'tabellen/route-all.csv'
output_filename = 'sorted_route.csv'

# Anzahl der Zahlen in jeder Zeile zählen und sortieren
row_lengths = count_row_length(filename)
sorted_rows = sorted(row_lengths, key=lambda x: x[0])  # Sortiere nach Anzahl der Zahlen

# Schreibe die sortierten Zeilen in eine neue Datei
write_sorted_rows(sorted_rows, output_filename)
