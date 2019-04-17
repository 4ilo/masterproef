import cv2
import osmnx as ox
import networkx as nx


class MapRenderer:
    def __init__(self, map_path, start_node=-137971):
        self.G = ox.graph_from_file(map_path, name="Map", retain_all=True, simplify=False)
        ox.config(imgs_folder="data/plot")
        self.start = start_node

    def show_route(self, end_node):
        """
        Show map and render route from start to end_node
        :param end_node: Node id of current location
        :return: Matplotlib figure
        """
        route = nx.shortest_path(self.G, self.start, end_node, weight='length')

        ox.plot_graph_route(self.G, route, node_size=0, show=False, save=True, filename="output", file_format="png")
        fig = cv2.imread("data/plot/output.png")

        return fig
