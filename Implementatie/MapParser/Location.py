
class Location:

    def __init__(self, loc):
        self._node = loc.pop('node')
        self.id = loc.pop('id')
        loc.pop('type')

        self.objects = {}

        # Get all objects
        for key, val in loc.items():
            self.objects.update({int(key): float(val)})

    def __repr__(self):
        return "Loc<{}>".format(self.id)
