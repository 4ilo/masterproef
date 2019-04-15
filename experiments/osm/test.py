import osmnx as ox

G = ox.graph_from_file("amk_copy.osm", name="test")
ox.plot_graph(G)
#test = ox.graph_to_gdfs(G)
#ox.plot_shape(ox.project_gdf(test))
