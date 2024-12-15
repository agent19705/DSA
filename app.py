from flask import Flask, render_template, request
import sys

app = Flask(__name__)

# Number of zones
V = 7

# Adjacency matrix representing the city graph
graph = [
    [0, 2, 0, 0, 1, 0, 0],
    [2, 0, 1, 0, 2, 0, 0],
    [0, 1, 0, 3, 0, 1, 0],
    [0, 0, 3, 0, 1, 0, 0],
    [1, 2, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0]
]

# Emergency zone mapping
EMERGENCY_MAP = {
    1: {"name": "Fire Station", "src": 4},
    2: {"name": "Hospital", "src": 2},
    3: {"name": "Police Station", "src": 3},
    4: {"name": "Residential Area 1", "src": 0},
}

# Dijkstra's algorithm to find shortest paths
def dijkstra(graph, src):
    dist = [sys.maxsize] * V
    dist[src] = 0
    processed = [False] * V

    for _ in range(V):
        min_index = -1
        min_distance = sys.maxsize
        for i in range(V):
            if not processed[i] and dist[i] < min_distance:
                min_distance = dist[i]
                min_index = i
        u = min_index
        processed[u] = True

        for v in range(V):
            if graph[u][v] > 0 and not processed[v] and dist[u] != sys.maxsize:
                new_distance = dist[u] + graph[u][v]
                if new_distance < dist[v]:
                    dist[v] = new_distance

    return dist

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        emergency_type = int(request.form.get("emergency_type"))
        if emergency_type in EMERGENCY_MAP:
            src = EMERGENCY_MAP[emergency_type]["src"]
            emergency_name = EMERGENCY_MAP[emergency_type]["name"]

            # Run Dijkstra's algorithm
            distances = dijkstra(graph, src)

            # Format results for rendering
            result = {
                "emergencyType": emergency_name,
                "src": src,
                "distances": {i: distances[i] for i in range(V)}
            }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
