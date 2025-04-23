from flask import Flask, render_template, request
import heapq

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form_type = request.form.get("form_type")
        print("Form Type:", form_type)

        if form_type == "init":
            nodes = int(request.form.get("nodes"))
            edges = int(request.form.get("edges"))
            print(f"Number of Nodes: {nodes}, Number of Edges: {edges}")
            return render_template("index.html", form_type="init", nodes=nodes, edges=edges)

        elif form_type == "visualize":
            try:
                num_nodes = int(request.form.get("num_nodes"))
                num_edges = int(request.form.get("num_edges"))
                graph = {i: [] for i in range(1, num_nodes + 1)}

                for i in range(num_edges):
                    u = int(request.form.get(f"u{i}"))
                    v = int(request.form.get(f"v{i}"))
                    w = int(request.form.get(f"w{i}"))
                    graph[u].append((v, w))

                    print(f"Edge {i}: From {u} to {v} with weight {w}")

                source = int(request.form.get("source"))
                target = int(request.form.get("target"))
                print(f"Source: {source}, Target: {target}")

                distance, path = dijkstra(graph, source, target)
                print("Shortest Path:", path, "| Distance:", distance)

                path_edges = list(zip(path, path[1:]))

                return render_template("index.html",
                    form_type="init",
                    nodes=num_nodes,
                    edges=num_edges,
                    path=path,
                    distance=distance,
                    path_edges=path_edges
                )
            except Exception as e:
                print("An error occurred:", e)
                return render_template("index.html", error=str(e))
    
    return render_template("index.html")


def dijkstra(graph, start, end):
    pq = [(0, start, [])]
    visited = set()

    while pq:
        (dist, current, path) = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]
        if current == end:
            return dist, path
        for neighbor, weight in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(pq, (dist + weight, neighbor, path))

    return float('inf'), []  # No path found


if __name__ == "__main__":
    app.run(debug=True)
