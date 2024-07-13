import os

import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities


# Get the directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))

# Define file paths relative to the project root directory
input_file_path = os.path.join(
    project_root, "output", "20240713-095103", "artifacts", "summarized_graph.graphml"
)
output_file_dir = os.path.join(
    project_root, "output", "20240713-095103", "post_artifacts"
)
os.makedirs(output_file_dir, exist_ok=True)


def assign_colors(G):
    node_color_map = {
        '"CONCEPT"': "cyan",
        '"EVENT"': "orange",
        '"ROLE"': "red",
        '"ORGANIZATION"': "blue",
        '"LOCATION"': "green",
        '"PERSON"': "magenta",
    }

    for n, attr in G.nodes(data=True):
        node_type = attr.get("type")
        if node_type in node_color_map:
            G.nodes[n]["color"] = node_color_map[node_type]
        else:
            G.nodes[n]["color"] = "grey"

    for u, v, d in G.edges(data=True):
        weight = d.get("weight", 0)
        if weight > 1:
            G.edges[u, v]["color"] = "black"
        else:
            G.edges[u, v]["color"] = "grey"


if __name__ == "__main__":
    # Load GraphML file
    G = nx.read_graphml(input_file_path)
    assign_colors(G)

    # Select nodes based on its types
    node_types = (
        # '"CONCEPT"'
        # '"EVENT"',
        # '"ROLE"',
        '"ORGANIZATION"',
        # '"LOCATION"',
        '"PERSON"',
    )
    filtered_nodes = [
        n for n, attr in G.nodes(data=True) if attr.get("type") in node_types
    ]
    types_subgraph = G.subgraph(filtered_nodes)
    certain_node_types_path = os.path.join(
        output_file_dir,
        "1.1_filtered_summarized_graph_node_types.graphml",
    )
    nx.write_graphml(types_subgraph, certain_node_types_path)

    # Detect communities using the greedy modularity communities algorithm
    communities = list(greedy_modularity_communities(G, weight="weight"))
    selected_community = communities[0]
    communities_subgraph = G.subgraph(selected_community)

    greedy_modularity_communities_path = os.path.join(
        output_file_dir, "1.2_summarized_graph_greedy_modularity_communities.graphml"
    )
    nx.write_graphml(communities_subgraph, greedy_modularity_communities_path)

    filtered_edges = [
        (u, v) for u, v, d in types_subgraph.edges(data=True) if d.get("weight", 0) > 1
    ]
    filtered_graph = G.edge_subgraph(filtered_edges)
    weight_path = os.path.join(
        output_file_dir,
        "1.3_filtered_summarized_graph_weight_greater_than_1.graphml",
    )
    nx.write_graphml(filtered_graph, weight_path)
