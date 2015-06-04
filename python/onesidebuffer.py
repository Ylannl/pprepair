import sys
import pprint
from shapely.geometry import Polygon
from shapely.geometry import LineString
from shapely.geometry import asShape
from shapely.geometry import mapping
from shapely.ops import cascaded_union, linemerge, polygonize
import fiona
import math

# infile = '/Users/hugo/Dropbox/data/ELF/edge-matching/ELF_IB_Master/ELFIB-NO.shp'
# infile = '/Users/hugo/Dropbox/data/pprepair/edgematching/v2/intl-boundaries/belu.shp'

infile  = sys.argv[1]
outfile = infile[:-4] + '.p.shp'

BUFFERSIZE = 0.2

c = fiona.open(infile, 'r')
print "Number of features:", len(c)
cout = c.schema
cout['geometry'] = 'Polygon'

lsL = []
for each in c:
    lsL.append(asShape(each['geometry']))
f = each
#-- the line needs to be *one* line, and simple
lmerge = linemerge(lsL)
assert(lmerge.geom_type == 'LineString')
assert(lmerge.is_simple == True)


def offset():
    oleft = lmerge.parallel_offset(BUFFERSIZE, 'left')
    oright = lmerge.parallel_offset(BUFFERSIZE, 'right')
    assert(oleft.geom_type == 'LineString')
    assert(oright.geom_type == 'LineString')
    tmp = list(oleft.coords)
    tmp.reverse()
    pleft  = Polygon(list(lmerge.coords) + tmp)
    pright = Polygon(list(lmerge.coords) + list(oright.coords))
    save_geom_shp([pleft, pright])


def halfbuffer():
    #-- 1st: buffer with 'square ends'
    buf = lmerge.buffer(BUFFERSIZE, cap_style=3, join_style=1)
    nb = len(list(buf.exterior.coords))
    print nb

    #-- 2nd: elongate the input line to that it crosses the buffer created
    ns = elongate_line(lmerge.coords[1], lmerge.coords[0])
    ne = elongate_line(lmerge.coords[-2], lmerge.coords[-1])
    newline = list(lmerge.coords)
    newline.insert(0, ns)
    newline.append(ne)
    lmerge2 = LineString(newline)
    # print len(lmerge2.coords)
    assert(lmerge2.geom_type == 'LineString')
    assert(lmerge2.is_simple == True)

    # sys.exit()    

    # #-- 3rd: add the end vertices of the line to the polygon
    # buf = buf.union(lmerge)
    # print buf.geom_type
    # na = len(list(buf.exterior.coords))
    # print na

    # oring = list(buf.exterior.coords)
    # index2 = oring.index(lmerge.coords[-1])
    # index1 = oring.index(lmerge.coords[0])

    # if (index1 < index2):
    #     a = LineString(oring[index1:index2+1])
    #     tmp = oring[index2:] + oring[:index1+1]
    #     b = LineString(tmp)
    # else:
    #     tmp = oring[index1:] + oring[:index2+1]
    #     a = LineString(tmp)
    #     b = LineString(oring[index2:index1+1])
    #     print a
    #     print b
    # poly2 = list(polygonize([lmerge, a, b]))


def elongate_line(a, b):
    d = math.sqrt(math.pow(b[1] - a[1], 2) + math.pow(b[0] - a[0], 2))
    vlambda = 1.01 + (BUFFERSIZE/d)
    rx = (vlambda * b[0]) + ((1 - vlambda) * a[0])
    ry = (vlambda * b[1]) + ((1 - vlambda) * a[1])
    return (rx, ry)


def save_geom_shp(geoms):
    with fiona.open(outfile, 
                    'w',
                    driver=c.driver,
                    crs=c.crs,
                    schema=cout) as output:
        for g in geoms:
            f['geometry'] = mapping(g)
            output.write(f)
    print "Results written to", outfile

if __name__ == '__main__':
    offset()
    # halfbuffer()