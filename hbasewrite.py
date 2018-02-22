import happybase
import simplejson as sjson
import json
from datetime import datetime

connection = happybase.Connection('trafficdata0')
table = connection.table('table-Datatest')
file = open('boladatabola.json', 'r')
for key, item in file.iteritems():
    file['time'] = time
    datetime.strptime(time,'%Y-%m-%dT%H:%M')




    table.puttable.put(b'row-key', {b'vehicle:lineRef': b'value1', b'lat:location latitude':b'value2',
                                    b'lon:location longitude':b'value3', b'speed:speed':b'value4'}, timestamp=123456789)

    row = table.row(b'row-key')
