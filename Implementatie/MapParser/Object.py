
class Object:

    def __init__(self, object):
        self._node = object['node']
        self.id = int(object['id'])
        self.name = object['name']

    def __repr__(self):
        return "{}<{}>".format(self.name, self.id)
