import sys
import math
import Image
import urllib
import cStringIO

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

ulLat = float(sys.argv[1])
ulLon = float(sys.argv[2])
lrLat = float(sys.argv[3])
lrLon = float(sys.argv[4])
zoom = 13
baseaddress = 'http://tile.openstreetmap.org/'

upLeftTile = deg2num(ulLat, ulLon, zoom)
lowRightTile = deg2num(lrLat, lrLon, zoom)
minX = min(upLeftTile[0], lowRightTile[0])
maxX = max(upLeftTile[0], lowRightTile[0])
minY = min(upLeftTile[1], lowRightTile[1])
maxY = max(upLeftTile[1], lowRightTile[1])
print upLeftTile, lowRightTile
images = []
for x in range(minX, maxX + 1):
    imgs = []
    for y in range(minY, maxY + 1):
        URL = baseaddress + str(zoom) + '/' + str(x) + '/' + str(y) + '.png'
        print >> sys.stderr, URL
        img = Image.open(cStringIO.StringIO(urllib.urlopen(URL).read()))
        imgs.append(img)
        img.save(str(x) + '_' + str(y) + '.png')       
    images.append(imgs)
xsize = images[0][0].size[0]
ysize = images[0][0].size[1]
nX = maxX-minX+1
nY = maxY-minY+1
composite = Image.new('RGB', (nX*xsize, nY*ysize))
for i in range(0, nX):
    for j in range(0, nY):
        composite.paste(images[i][j], (i*xsize, j*ysize))
composite.save(sys.argv[5])
