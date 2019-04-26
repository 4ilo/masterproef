import osmnx as ox
import networkx as nx

# Read map
G = ox.graph_from_file("data/map.osm", name="Kaart", retain_all=True)

nodes = [-126565, -126574, -126583, -126592, -126601, -126610, -126619]

start = ox.get_nearest_node(G, (50.13554168794, 8.64772690044))

for node in nodes:
    route = nx.shortest_path(G, start, node, weight='length')
    fig, ax = ox.plot_graph_route(G, route, node_size=0, show=False)
    fig.show()
