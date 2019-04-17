
class Location:
    def __init__(self, loc, node_id):
        self._node = loc.pop('node')
        self.node_id = node_id
        self.id = loc.pop('id')
        loc.pop('type')

        self.objects = {}

        # Get all objects
        for key, val in loc.items():
            self.objects.update({int(key): float(val)})

    def __repr__(self):
        return "Node<{}>/Loc<{}>".format(self.node_id, self.id)
