import json
from django.shortcuts import render
from collections import deque
import networkx as nx
from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objs as go

def calculate_local_metric_basis(n):
    graph = {i: [] for i in range(n)}
    for i in range(n - 1):
        graph[i].append(i + 1)
        graph[i + 1].append(i)

    W_l = [i + 1 for i in range(1, n, 3)]
    if n % 3 != 0 and n not in W_l:
        W_l.append(n)

    distances_table = {v: bfs_distances(graph, v - 1, n) for v in W_l}
    return W_l, distances_table, graph

def bfs_distances(graph, start, n):
    distances = [-1] * n
    distances[start] = 0
    queue = deque([start])

    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if distances[neighbor] == -1:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)
    return distances

def plot_graph_plotly(n, W_l):
    G = nx.path_graph(n)
    pos = {i: (i, 0) for i in range(n)}

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=2, color='#888'),
        hoverinfo='none'
    )

    node_x, node_y = [], []
    node_color = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        color = 'red' if (node + 1) in W_l else 'blue'
        node_color.append(color)
        node_text.append(f"v{node+1}")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="bottom center",
        marker=dict(color=node_color, size=12, line=dict(width=2, color='black')),
        hoverinfo='text'
    )

    data = [edge_trace, node_trace]

    layout = go.Layout(
        showlegend=False,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400
    )

    fig = go.Figure(data=data, layout=layout)
    return json.dumps(fig, cls=PlotlyJSONEncoder)


def index_view(request):
    return render(request, 'graph_app/index.html')

def penerapan_view(request):
    return render(request, 'graph_app/penerapan.html')

def reference_view(request):
    return render(request, 'graph_app/reference.html')

def graph_view(request):
    if request.method == "POST":
        n = int(request.POST.get('n'))

        W_l, distances_table, graph = calculate_local_metric_basis(n)
        Wl_labeled = [f"v{v}" for v in W_l]

        distances_info = {}
        for i in range(1, n + 1):
            distances = [distances_table[v][i - 1] for v in W_l]
            key = f"r(v{i}|Wl)"
            distances_info[key] = tuple(distances)

        plotly_json = plot_graph_plotly(n, W_l)

        return render(request, 'graph_app/graph_result.html', {
            'Wl': Wl_labeled,
            'distances_info': distances_info,
            'plotly_data': plotly_json,
        })
    
    return render(request, 'graph_app/graph_form.html')

