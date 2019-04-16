
import xml.etree.ElementTree as ET
from .Object import Object
from .Location import Location


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


def parse_map(filename):
    """ Get object and location nodes """
    tree = ET.parse(filename)
    root = tree.getroot()

    objects = []
    locations = []

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
                            locations.append(Location(data))

    return objects, locations


