import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

# Excel-Datei einlesen
df = pd.read_excel("basisdatenb.xlsx")

# Graph initialisieren
G = nx.Graph()

# Knoten hinzufügen mit Attributen
for _, row in df.iterrows():
    name = row['Name']
    G.add_node(name,
               Abteilung=row['Abteilung'],
               Email=row['Email'],
               Interessen=row['Interessen'],
               Erfahrungsstufe=row['Erfahrungsstufe'])

# Kanten basierend auf Kontakten hinzufügen
for _, row in df.iterrows():
    name = row['Name']
    kontakte = row.get('Kontakte', '')
    if pd.isnull(kontakte):
        continue
    kontakte = [k.strip() for k in str(kontakte).split(',') if k.strip()]
    for kontakt in kontakte:
        if kontakt in G.nodes and kontakt != name:
            G.add_edge(name, kontakt)

# Labels für die Knoten erstellen
labels = {node: f"{node}\n{data['Abteilung']} | {data['Erfahrungsstufe']}" for node, data in G.nodes(data=True)}

# Graph zeichnen
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx_nodes(G, pos, node_color='lightgreen', node_size=800, edgecolors='black')
nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7)
nx.draw_networkx_labels(G, pos, labels, font_size=8)

plt.title("Teilnehmernetzwerk basierend auf Excel-Daten", fontsize=14)
plt.axis('off')
st.pyplot(plt.gcf())
plt.clf()  # optional, um die Figure zu leeren
