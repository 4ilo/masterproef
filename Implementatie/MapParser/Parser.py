
import xml.etree.ElementTree as ET
from .Object import Object
from .Location import Location
from .Way import Way


def convert(node):
    """
    Convert xml tags into dict
    :param node: XmlTree node
    :return: Dict
    """
    data = {
        'node': node
    }

    for tag in node:
        data.update({
            tag.get('k'): tag.get('v')
        })

    return data


def parse_way(node, locations):
    ids = {x.node_id: x for x in locations}
    node_list = []

    for nd in node.findall('nd'):
        if int(nd.get('ref')) in ids.keys():
            node_list.append(ids[int(nd.get('ref'))])

    if len(node_list):
        return Way(node_list)

    return False


def parse_map(filename):
    """ Get object, way and location nodes """
    tree = ET.parse(filename)
    root = tree.getroot()

    objects = []
    locations = []
    ways = []

    # Get nodes
    for child in root:
        if child.tag == 'node':
            for tag in child:
                if tag.tag == 'tag':
                    if tag.get('k') == 'type':
                        # Get this node
                        if tag.get('v') == 'object':
                            data = convert(child)
                            objects.append(Object(data))

                        elif tag.get('v') == 'location':
                            data = convert(child)
                            locations.append(Location(data, int(child.get('id'))))

    # Get ways
    for child in root:
        if child.tag == 'way':
            way = parse_way(child, locations)
            if way:
                ways.append(way)

    # Attach Objects to Locations
    for location in locations:
        location.link_objects(objects)

    return objects, locations, ways


