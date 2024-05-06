import matplotlib.pyplot as plt

# Daten einlesen
with open('tabellen/graph.csv', 'r') as f:
    data = f.readlines()

# Punkte und Verbindungen extrahieren
points = {}
connections = []
for line in data:
    line = line.strip().split(',')
    edge_number = int(line[0])
    edge_name = line[1]
    node_a = int(line[2])
    node_b = int(line[3])
    node_a_coords = (float(line[4]), float(line[5]))
    node_b_coords = (float(line[6]), float(line[7]))
    connections.append((node_a_coords, node_b_coords))
    points[node_a] = node_a_coords
    points[node_b] = node_b_coords

# Plot erstellen
plt.figure(figsize=(10, 8))  # Größe des Diagramms festlegen
for connection in connections:
    plt.plot([connection[0][0], connection[1][0]], [connection[0][1], connection[1][1]], marker='o', markersize=2)  # Punkte kleiner machen

# Punkte beschriften
for point_id, point in points.items():
    plt.text(point[0], point[1], str(point_id), fontsize=2)

# Achsen beschriften
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Graphische Darstellung von Verbindungen')

# Gitter hinzufügen
plt.grid(True)

# Diagramm speichern mit höherer Auflösung
plt.savefig('diagramme/graph.png', dpi=300)  # Höhere Auflösung (dots per inch)

# Plot anzeigen
plt.show()
