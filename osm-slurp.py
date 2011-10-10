from sys import stdin
from math import hypot, ceil

from shapely.geometry import Polygon

from Skeletron import network_multiline, multiline_polygon, polygon_rings, polygon_skeleton, skeleton_routes
from Skeletron.util import simplify_line
from Skeletron.input import ParserOSM
from Skeletron.draw import Canvas

p = ParserOSM()
g = p.parse(stdin.read())

print sorted(g.keys())

network = g[(u'Lakeside Drive', u'secondary')]

if not network.edges():
    exit(1)

lines = network_multiline(network)
poly = multiline_polygon(lines)
skeleton = polygon_skeleton(poly)
routes = skeleton_routes(skeleton)

# draw

points = [network.node[id]['point'] for id in network.nodes()]
xs, ys = map(None, *[(pt.x, pt.y) for pt in points])

xmin, ymin, xmax, ymax = min(xs), min(ys), max(xs), max(ys)

canvas = Canvas(900, 600)
canvas.fit(xmin - 50, ymax + 50, xmax + 50, ymin - 50)

for route in reversed(routes):
    line = simplify_line(route)

    canvas.line(line, stroke=(1, 1, 1), width=10)
    for (x, y) in line:
        canvas.dot(x, y, fill=(1, 1, 1), size=16)

    canvas.line(line, stroke=(1, .6, .4), width=6)
    for (x, y) in line:
        canvas.dot(x, y, fill=(1, .6, .4), size=12)

#for (v, w) in skeleton.edges():
#    line = list(skeleton.edge[v][w]['line'].coords)
#    canvas.line(line, stroke=(.4, .4, .4), width=2)

for ring in polygon_rings(poly):
    canvas.line(list(ring.coords), stroke=(.9, .9, .9))

for (a, b) in network.edges():
    pt1, pt2 = network.node[a]['point'], network.node[b]['point']
    line = [(pt1.x, pt1.y), (pt2.x, pt2.y)]
    canvas.line(line, stroke=(0, 0, 0))

for point in points:
    canvas.dot(point.x, point.y, fill=(0, 0, 0))

canvas.save('look.png')
