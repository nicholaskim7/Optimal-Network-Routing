import heapq
from typing import Dict, List
import networkx as nx
import matplotlib.pyplot as plt

#weighted and uni-directed graph dijkstras
def shortestPath(n: int, edges: List[List[int]], src: int, is_latency: bool) -> Dict[int, int]:
        adj = {} #convert edges to adjacency matrix

        for i in range(n): #for every node map to empty list
            adj[i] = []
        
        for s, d, weight in edges: #map every source to the destination/weight
            adj[s].append([d,weight])
            #adj[d].append([s, weight]) #for bi directed graph
        
        shortest = {} #map vertex to dist of shortest path
        previous = {}

        minHeap = [[0, src]] #initialize minheap

        while minHeap:
            w1, n1 = heapq.heappop(minHeap)
            if n1 in shortest: #already found shortest path for this node
                continue

            shortest[n1] = w1 #if we havent found shortest path we say the total to reach this node

            for n2, w2 in adj[n1]: #go through the neighbors of that node
                if n2 not in shortest:  # Only process unvisited nodes
                    new_weight = w1 + w2 if is_latency else -(w1 + w2)
                    heapq.heappush(minHeap, (new_weight, n2))

                    # Update the previous node for path reconstruction
                    if n2 not in previous or new_weight < shortest.get(n2, float('inf')):
                        previous[n2] = n1
        
        for i in range(n): #nodes we didnt visit must be assigned -1 dist
            if i not in shortest:
                shortest[i] = -1

        return shortest, previous


def visualize_graph(n: int, edges: List[List[int]], src: int, shortest: Dict[int, int], previous: Dict[int, int], is_latency: bool):
    G = nx.DiGraph()

    # Add nodes
    for i in range(n):
        G.add_node(i)

    # Add edges with weights
    for s, d, weight in edges:
        G.add_edge(s, d, weight=weight)

    pos = nx.spring_layout(G, seed=42)

    # Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')

    # Draw edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Highlight the optimal path
    optimal_edges = []
    for dest in shortest:
        if dest != src and shortest[dest] != -1:
            # Backtrack from the destination to the source
            current = dest
            while current in previous:
                prev = previous[current]
                optimal_edges.append((prev, current))
                current = prev

    # Draw the optimal path in red
    nx.draw_networkx_edges(G, pos, edgelist=optimal_edges, edge_color='red', width=2)

    # Display the plot
    label = "Latency" if is_latency else "Bandwidth"
    plt.title(f"Shortest Path Visualization ({label})", fontsize=16)
    plt.show()


def apply_no_transit_policy(edges: List[List[int]], no_transit_nodes: List[int]) -> List[List[int]]:
    filtered_edges = []
    for src, dest, weight in edges:
        if src not in no_transit_nodes or dest == src:
            filtered_edges.append([src, dest, weight])
    return filtered_edges



def main():
    n = int(input("Enter number of routers: "))
    e = int(input("Enter number of connections (edges): "))
    edges = []

    is_latency_input = input("minimize latency(l) or maximize bandwith(b): ").strip().lower()
    if is_latency_input == "l":
        is_latency = True
    elif is_latency_input == "b":
        is_latency = False
    else:
        print("Invalid input. Defaulting to minimizing latency.")
        is_latency = True


    for i in range(e):
        node_input = input("Enter the src router, dest router, and weight separated by spaces: ")
        node_list = list(map(int, node_input.split()))
        edges.append(node_list)
    
    src = int(input("Enter source node: "))

    transit_policy = str(input("Allow transit packets (y/n):"))
    if transit_policy == "n":
        no_transit_nodes = list(map(int, input("Enter no-transit routers (space-separated): ").split()))
        edges = apply_no_transit_policy(edges, no_transit_nodes)
        


    result, previous = shortestPath(n, edges, src, is_latency)

    print("\nOptimal Path Results:")
    for router, cost in result.items():
        if not is_latency and cost != -1:
            cost = -cost
            label = "bandwith"
        else:
            label = "latency"

        print(f"Router {router} - {'Unreachable' if cost == -1 else f'{cost} ({label})'}")
    
    # Visualize the graph and results
    visualize_graph(n, edges, src, result, previous, is_latency)


if __name__ == "__main__":
    main()