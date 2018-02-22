from sys import argv
import math
import Image, ImageDraw, ImageFont
from datetime import datetime
import StringIO
import json

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

route = argv[9]
vehicle = argv[10] if len(argv) == 11 else None
speedsLocs = []
times = []
with open(argv[1], 'r') as infile:
    databuf = StringIO.StringIO()
    for line in infile:
        databuf.write(line)
        if line == '}\n':
            databuf.seek(0)
            data = json.load(databuf)
            databuf.close()
            databuf = StringIO.StringIO()
            for trip in data['body']:
                bus = trip['monitoredVehicleJourney']
                if bus['lineRef'] == route:
                    if vehicle == None:
                        vehicle = bus['vehicleRef']
                    if vehicle == bus['vehicleRef']:
                        t = datetime.strptime(trip['recordedAtTime'],
                                              '%Y-%m-%dT%H:%M:%S.%f+03:00')
                        if len(times) == 0 or times[-1] != t:
                            speedsLocs.append([float(bus['speed']),
                                  [float(bus['vehicleLocation']['latitude']),
                                   float(bus['vehicleLocation']['longitude'])]])
                            times.append(t)

mapImg = Image.open(argv[2])
draw = ImageDraw.Draw(mapImg)
zoom = int(argv[3])
minX = int(argv[4])
minY = int(argv[5])
maxX = int(argv[6])
maxY = int(argv[7])
tileWidth = mapImg.size[0]/(maxX-minX+1)
tileHeight = mapImg.size[1]/(maxY-minY+1)
fnt = ImageFont.load_default()
bbs = []
for spLoc in speedsLocs:
    lat, lon = spLoc[1]
    X, Y = deg2num(lat, lon, zoom)
    ulLat, ulLon = num2deg(X, Y, zoom)
    lrLat, lrLon = num2deg(X+1, Y+1, zoom)
    inTileY = (lat-ulLat)*tileHeight/(lrLat-ulLat)
    inTileX = (lon-ulLon)*tileWidth/(lrLon-ulLon)
    x = tileWidth*(X-minX) + inTileX
    y = tileWidth*(Y-minY) + inTileY
    txt = str(spLoc[0])
    w, h = draw.textsize(txt, font=fnt)
    bb = [x-w/2, y-h/2, x+w-1-w/2, y+h-1-h/2]
    ok = True
    for prevBB in bbs:
        if (prevBB[0] < bb[2]) and (bb[0] < prevBB[2]) and (prevBB[1] < bb[3]) and (bb[1] < prevBB[3]):
            ok = False
            break;
    if ok:
        draw.text([x-w/2, y-h/2], txt, font=fnt, fill='black')
        bbs.append(bb)

mapImg.show()
mapImg.save(argv[8])
