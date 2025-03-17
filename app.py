import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import pandas as pd
import networkx as nx

# Загружаем данные
file_path = "/mnt/data/Силы связи для карты.xlsx"
df = pd.read_excel(file_path, sheet_name="Сила связи")
df.rename(columns={"Unnamed: 0": "Эксосистема"}, inplace=True)

# Создаём граф
G = nx.Graph()

# Добавляем узлы (экосистемы и категории)
ecosystems = df["Эксосистема"].unique()
categories = df.columns[1:]
for eco in ecosystems:
    G.add_node(eco, type="eco")
for cat in categories:
    G.add_node(cat, type="category")

# Добавляем связи (рёбра) с весами
edges = []
for _, row in df.iterrows():
    eco = row["Эксосистема"]
    for cat in categories:
        weight = row[cat]
        if weight > 0:
            G.add_edge(eco, cat, weight=weight)
            edges.append((eco, cat, weight))

# Переводим граф в формат Dash Cytoscape
elements = []
for node in G.nodes(data=True):
    elements.append({"data": {"id": node[0], "label": node[0]}})
for edge in G.edges(data=True):
    elements.append({"data": {"source": edge[0], "target": edge[1], "weight": edge[2]['weight']}})

# Инициализация Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Карта экосистем"),
    
    cyto.Cytoscape(
        id='network-graph',
        elements=elements,
        layout={'name': 'cose'},
        style={'width': '100%', 'height': '700px'},
        stylesheet=[
            {'selector': 'node', 'style': {'content': 'data(label)', 'text-valign': 'center', 'color': 'white', 'background-color': '#0074D9'}},
            {'selector': 'edge', 'style': {'width': 'data(weight)', 'line-color': '#AAAAAA'}}
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
