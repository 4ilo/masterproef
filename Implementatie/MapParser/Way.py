
class Way:
    def __init__(self, node_list):
        self.node_list = node_list

    def __repr__(self):
        out = ""
        for node in self.node_list:
            out += "<{}>;".format(node.node_id)

        return out