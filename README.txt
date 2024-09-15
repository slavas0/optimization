Starten: run.py
Parameter: instanzindx, indexfile zeit_oder_zeile, instance_time, weight_A, weight_B, num_elements, coef
Ergebnisse: in Ordner ergebnisse/ als Visualisierung, in Ergebnisse.csv die Routenbeschreibung
Eingabe: durch test.csv in tabellen/ im Format von data-all.csv


Dieses Projekt wird durch die run.py ausgeführt. Die Ergebnisse werden in den Ordner "ergebnisse/" ausgegeben. 
Die Bearbeitung der Parameter und des Inputs erfolgt am Anfang der run.py.

Neue Instanzen können in einer eigenen .csv Datei im Format der data-all.csv eingefügt werden. Durch die String Variable 
indexfile kann diese neue Datei ausgesucht werden und mit instanzindx die Zeilen ausgewählt.

Beispiel: Instanzen stehen in test.csv im Ordner "tabellen/" Zeile 7: 
Parameter: 
instanzindx = 7
indexfile = "tabellen/test.csv"
zeit_oder_zeile = True


Die folgende vollständige Liste der Parameter kann am Anfang der Datei run.py angepasst werden und werden kurz beschrieben 
und zusätzlich im Code kurz kommentiert: 

instance_time, instanzindx, zeit_oder_zeile
Eine Instanz kann dem Programm auf zwei Arten übergeben werden. Es kann entweder 
der Startzeitpunkt mit Hilfe des Parameters instance_time angegeben werden, oder es
wird der Zeilenindex im Parameter instanzindx übergeben. Der Parameter zeit_oder_zeile
wird auf True gesetzt, wenn die erste Möglichkeit genutzt werden soll, sonst auf False.
weight_A, weight_B

weight_A, weight_B
In Zeile 9-10 werden die Gewichtungen für Schnelligkeit und Ähnlichkeit mit Hilfe der
Parameter weight_A, weight_B festgelegt.

num_elements
Der Parameter num_elements gibt an, wie viele Routen aus dem ersten Cluster als 
Ähnlichkeitsmaß in Schritt 4 genommen werden sollen.

coef
Es besteht außerdem die Möglichkeit, den verschiedenen Regionen eine Gewichtung mit Hilfe der Liste coef zuzuordnen.

Dauer: etwa 11m40s für 10 Instanzen -> 1m10s pro Instanz
Hardware 5800x, 16GB DDR4, braucht 4,5GHz Boosttakt und 4GB verfügbaren Arbeitspeicher.
Das Programm benutzt nur 4 Threads (auf 2 Kernen).