#!/usr/bin/env python3
assert __name__=='__main__'

import os
import sys
import datetime
import pathlib
import shutil

class Resource:
    def __init__(self, key):
        self._key = key
        self._val = os.environ.get(self._key)
        self._path = self._val and pathlib.Path(self._val)
    def check(self):
        print( "${%s} is [%s]" % (self._key, self._val) )
        if not self._val:
            return print('${%s}: not defined' % self._key )
        elif not self._path:
            return print('${%s}: not a path' % self._key )
        elif not self._path.is_dir():
            return print('${%s} is not a directory' % self._key )
        else:
            return True
    def path(self):
        self.check() or exit()
        return self._path

DEVICE = Resource( 'WS852_DEVICE_ROOT' )
UPLOAD = Resource( 'WS852_UPLOAD_DIR' )


def NATIVE_FILES():
    return DEVICE.path().glob('**/[0-9][0-9][0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9]*.MP3')

def FIXED_FILES():
    return DEVICE.path().glob('**/*.ws852.mp3')

def cmd_rename():
    for path in NATIVE_FILES():
        mtime = os.path.getmtime(str(path))
        stamp = datetime.datetime.fromtimestamp(mtime).strftime('%Y%m%dT%H%M%S')
        serial = path.name.split('.')[0].split('_')[1]
        newname = '%s.[serial-%s].ws852.mp3' % (stamp, serial)
        newpath = path.parent/newname
        print('rename: %s -> %s' % (path,newpath))
        path.rename(newpath)

def cmd_upload():
    for path in FIXED_FILES():
        newpath = UPLOAD.path()/path.name
        print('%s -> %s' % (path,newpath))
        shutil.move(path,newpath)


def main():
    cmd = sys.argv[-1]
    if False: pass
    elif cmd == 'rename':
        cmd_rename()
    elif cmd == 'upload':
        cmd_upload()
    elif cmd == 'check':
        UPLOAD.check()
        DEVICE.check() or print('device not mounted')
    else:
        print(USAGE)


USAGE="""
WS852 : Handle files on the Olympus WS-852 voice recorder.

USAGE:
        %s SUBCOMMAND
""" % pathlib.Path(sys.argv[0]).name + """
SUBCOMMANDS:
        rename   - rename all raw voicefiles in device to show timestamp
        upload   - move all renamed files to ${WS852_UPLOAD_DIR} (if well defined)
        check    - check whether environment is defined and device is attached
        help     - print this help document

PRECONDITIONS:
        ${WS852_DEVICE_ROOT} must be set to the root folder of the mounted device.
        ${WS852_UPLOAD_DIR} must be set to an upload folder.

NOTES:
        Voice files created natively have filenames matching:
                "YYMMDD_NNNN.MP3"
        where
                - YYMMDD indicates the recording date
                - NNNN indicates and incrementing serial number
                - MP3 is the literal 'MP3' (uppercase)

        All such files will be renamed in place to have filenames matching:
                "YYYYMMDD.HHMMSS.{serial:NNNN}.ws852.mp3"
        where
                - YYYYMMDD.HHMMSS is a timestamp indicating the file creation time
                - NNNN is the NNNN from the original filename

        The timestamp may reflect the time the voice recording began or the time the
        voice recording ended. There is no guarantee of which of these times will be
        used. Be careful interpreting the timestamp with very long recordings.
"""


main()
