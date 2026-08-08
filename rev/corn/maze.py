import networkx as nx
import random

def generate_eulerian_graph(
    n: int,
    extra_cycle_probability: float = 0.7,
    seed: int | None = None,
) -> nx.Graph:
    rng = random.Random(seed)

    # Randomize the initial Hamiltonian cycle.
    vertices = list(range(n))
    rng.shuffle(vertices)

    graph = nx.Graph()
    graph.add_nodes_from(vertices)

    for index in range(n):
        graph.add_edge(vertices[index], vertices[(index + 1) % n])

    if n >= 3 and rng.random() < extra_cycle_probability:
        available = [node for node in graph if graph.degree(node) == 2]

        for _ in range(1_000):
            cycle_size = rng.randint(3, len(available))
            extra_cycle = rng.sample(available, cycle_size)
            rng.shuffle(extra_cycle)

            candidate_edges = [
                (
                    extra_cycle[index],
                    extra_cycle[(index + 1) % cycle_size],
                )
                for index in range(cycle_size)
            ]

            if (
                len({frozenset(edge) for edge in candidate_edges})
                != cycle_size
            ):
                continue

            if any(graph.has_edge(u, v) for u, v in candidate_edges):
                continue

            graph.add_edges_from(candidate_edges)
            break

    return graph


def verify_eulerian_graph(graph: nx.Graph, max_degree: int = 4) -> bool:
    connected = nx.is_connected(graph)
    all_degrees_even = all(
        degree % 2 == 0 for _, degree in graph.degree()
    )
    degree_limit_respected = all(
        degree <= max_degree for _, degree in graph.degree()
    )
    networkx_result = nx.is_eulerian(graph)

    print(f"Nodes:                 {graph.number_of_nodes()}")
    print(f"Edges:                 {graph.number_of_edges()}")
    print(f"Connected:             {connected}")
    print(f"All degrees even:      {all_degrees_even}")
    print(f"Maximum degree <= {max_degree}: {degree_limit_respected}")
    print(f"NetworkX is_eulerian:  {networkx_result}")

    return (
        connected
        and all_degrees_even
        and degree_limit_respected
        and networkx_result
    )

n = 100
p = 0.8

while True:
    graph = generate_eulerian_graph(n, p)
    if verify_eulerian_graph(graph):
        break

m = {}
fnames = ["up", "down", "left", "right"]
fshort = ["w", "s", "a", "d"]
for node in range(n):
    m[node] = {}
    for i, neighbor in enumerate(graph.neighbors(node)):
        m[node][neighbor] = (fnames[i], fshort[i])

with open("maze_gen.cpp", "w") as f:
    f.write("struct Node* mov_null() { return nullptr; }\n")

    names = []
    for node in range(n):
        nnames = []
        for i, neighbor in enumerate(graph.neighbors(node)):
            nnames.append(f"mov_{node}_{i}")
            f.write(f"struct Node* mov_{node}_{i}() {{ graph[{node}].{m[node][neighbor][0]} = mov_null; graph[{neighbor}].{m[neighbor][node][0]} = mov_null; return &graph[{neighbor}]; }}\n")
        for _ in range(4 - len(nnames)):
            nnames.append(f"mov_null")
        names.append(nnames)

    f.write("\n")
    f.write("void genmaze() {\n")
    for i, nnames in enumerate(names):
        f.write(f"\tgraph[{i}] = Node({i}, {', '.join(nnames)});\n")
    f.write("}\n")

with open("solution_gen.txt", "w") as f:
    path = [x for x, y in nx.eulerian_circuit(graph)]
    print(f"Path length: {len(path)}")
    start = path[0]
    prev = path[0]
    f.write(f"{prev}\n")
    for node in path[1:]:
        f.write(f"{m[prev][node][1]}\n")
        prev = node
    f.write(f"{m[prev][start][1]}\n")
    f.write("q")
