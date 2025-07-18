import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
from pyvis.network import Network

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
# plt.figure(figsize=(14, 10))
# pos = nx.spring_layout(G, seed=42)
# nx.draw_networkx_nodes(G, pos, node_color='lightgreen', node_size=800, edgecolors='lightgreen')
# nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7)
# nx.draw_networkx_labels(G, pos, labels, font_size=5)

# plt.title("Teilnehmernetzwerk basierend auf Excel-Daten", fontsize=14)
# Pyvis Netzwerk erstellen
net = Network(notebook=False, width="1800px", height="1000px", bgcolor="#ffffff", font_color="black")

# Knoten hinzufügen mit Hover-Infos
for _, row in df.iterrows():
    name = row['Name']
    abt = row['Abteilung']
    email = row['Email']
    inter = row['Interessen']
    stufe = row['Erfahrungsstufe']
    tooltip = f"""
    Name: {name}
    Abteilung: {abt}
    Email: {email}
    Interessen: {inter}
    Erfahrungsstufe: {stufe}
    """
    net.add_node(name, label=name, title=tooltip)

# Kanten hinzufügen
for _, row in df.iterrows():
    name = row['Name']
    kontakte = row.get('Kontakte', '')
    if pd.isnull(kontakte):
        continue
    kontakte = [k.strip() for k in str(kontakte).split(',') if k.strip()]
    for kontakt in kontakte:
        if kontakt in df['Name'].values and kontakt != name:
            net.add_edge(name, kontakt)

# Netzwerk als HTML speichern und in Streamlit anzeigen
st.set_page_config(layout="wide")
net.write_html("netzwerk.html")
with open("netzwerk.html", "r", encoding="utf-8") as f:
    html = f.read()
st.components.v1.html(html, height=1000, width=1800, scrolling=False)
plt.axis('off')
st.pyplot(plt.gcf())
plt.clf()  # optional, um die Figure zu leeren
