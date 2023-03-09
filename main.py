def read(file):
    with open(file) as f:
        lines = f.read().splitlines()

    C, R, S = map(int,lines[0].split())
    sneake_len = list(map(int,lines[1].split()))

    matrix = [[0 for _ in range(C)] for _ in range(R)]
    wormholes_coord = []

    for i in range(R):
        l = []
        for j,schifo in enumerate(list(lines[i+2].split())):
            if schifo == "*":
                wormholes_coord.append((i,j))
            l.append(schifo)
        matrix[i] =l



    return C, R, S, matrix, wormholes_coord


output = ""
with open("output.txt","w") as f:
    f.write(output)


def print_distance(distance, src):
    print(f"Vertex\tShortest Distance from vertex {src}")
    for i, d in enumerate(distance):
        print(f"{i}\t\t{d}")


def check_negative_cycle(
    graph, distance, edge_count: int
):
    for j in range(edge_count):
        u, v, w = (graph[j][k] for k in ["src", "dst", "weight"])
        if distance[u] != float("inf") and distance[u] + w < distance[v]:
            return True
    return False


def bellman_ford(
    graph, vertex_count: int, edge_count: int, src: int
):
    """
    Returns shortest paths from a vertex src to all
    other vertices.
    >>> edges = [(2, 1, -10), (3, 2, 3), (0, 3, 5), (0, 1, 4)]
    >>> g = [{"src": s, "dst": d, "weight": w} for s, d, w in edges]
    >>> bellman_ford(g, 4, 4, 0)
    [0.0, -2.0, 8.0, 5.0]
    >>> g = [{"src": s, "dst": d, "weight": w} for s, d, w in edges + [(1, 3, 5)]]
    >>> bellman_ford(g, 4, 5, 0)
    Traceback (most recent call last):
     ...
    Exception: Negative cycle found
    """
    distance = [float("inf")] * vertex_count
    distance[src] = 0.0

    for _ in range(vertex_count - 1):
        for j in range(edge_count):
            u, v, w = (graph[j][k] for k in ["src", "dst", "weight"])

            if distance[u] != float("inf") and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w

    negative_cycle_exists = check_negative_cycle(graph, distance, edge_count)
    if negative_cycle_exists:
        raise Exception("Negative cycle found")

    return distance

def movimenti_possibili(i,j,move,R,C):
    if move=="R":
        j = (j + 1) % C
    elif move=="L":
        j = (j - 1) % C
    elif move == "D":
        i = (i + 1) % R
    else:
        i = (i - 1) % R


    return i,j

def movimenti_warmholes():
    
    pass

if __name__ == "__main__":

    C, R, S, matrix, wormholes_coord = read("00-example.txt")

    print('# columns:', C)
    print('# raws:', R)
    print('# snakes:', S)
    print(matrix)
    #number of vertices
    V = C*R
    num_wormhole = len(wormholes_coord)
    #number of edges
    E = (V-num_wormhole)*4 + num_wormhole*4 - 1
    print(E)

    graph = []
    for i in range(R):
        for j in range(C):
            if matrix[i][j] == "*":
                for (n_i,n_j) in wormholes_coord:
                    d = {}
                    d["src"] = i * C + j
                    #consideriamo anche il caso src=dst (vertice che si collega a sé stesso)
                    for move in ["U","D","L","R"]:
                        n_i, n_j = movimenti_possibili(n_i,n_j,move,R,C)
                        if (n_i,n_j) in wormholes_coord:
                            continue
                        d["dst"] = n_i * C + n_j
                        
                        d["weight"] = matrix[i][j] + matrix[n_i][n_j]
                        graph.append(d)
            d = {}
            d["src"] = i * C + j
            for move in ["U","D","L","R"]:
                n_i, n_j = movimenti_possibili(i,j,move,R,C)
                d["dst"] = n_i * C + n_j
                d["weight"] = matrix[i][j] + matrix[n_i][n_j]
            
                graph.append(d)
    print(len(graph))
    source = int(input("\nEnter shortest path source:").strip())
    shortest_distance = bellman_ford(graph, V, E, source)
    print_distance(shortest_distance, 0)