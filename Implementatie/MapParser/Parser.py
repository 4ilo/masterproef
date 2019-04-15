
import xml.etree.ElementTree as ET


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

    nodes = []

    for child in root:
        if child.tag == 'node':
            for tag in child:
                if tag.tag == 'tag':
                    if tag.get('k') == 'type':
                        # Get this node
                        nodes.append(convert(child))

    return nodes


