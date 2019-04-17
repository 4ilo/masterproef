from MapParser import *

objects, locations, ways = parse_map("data/map.osm")

print(objects)
print(locations)
print(ways)
