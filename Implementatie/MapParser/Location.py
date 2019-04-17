
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

    def split(self, filters):
        """ Split objects into categories """
        splits = {}

        for f in filters:
            splits.update({
                f: [x for x, _ in self.objects.items() if x.name == f]
            })

        return splits

    def link_objects(self, objects):
        """ Replace object ids with references to the real objects """
        new_dict = {}

        for key, value in self.objects.items():
            new_dict.update({
                list(filter(lambda x: x.id == key, objects))[0]: value
            })

        self.objects = new_dict