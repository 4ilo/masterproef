
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

        back = self.node_list[index-1]
        if len(back.objects) == 0:
            back = node

        return back, node, self.node_list[index+1]

