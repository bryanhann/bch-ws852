assert __name__=='__main__'

import os
import sys
import datetime

def rename( fname ):
    ts = os.path.getmtime(fname)
    dt = datetime.datetime.fromtimestamp(ts)
    timestamp = dt.strftime('%Y%m%dT%H%M%S')
    newname = '%s.ws852.mp3' % timestamp
    return newname

if __name__=='__main__':
    print( rename( sys.argv[1] ) )

