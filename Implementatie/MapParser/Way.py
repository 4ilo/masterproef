
class Way:
    def __init__(self, node_list):
        self.node_list = node_list

    def __repr__(self):
        out = ""
        for node in self.node_list:
            out += "<{}>;".format(node.node_id)
        return out

    def get_neighbours(self, node):
        index = self.node_list.index(node)
        return tuple(self.node_list[index-1:index+2])

