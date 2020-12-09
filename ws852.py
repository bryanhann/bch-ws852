assert __name__=='__main__'
from pathlib import Path
import os
import sys
import datetime
USAGE="""
WS852 : Handle files on the Olympus WS-852 voice recorder.

USAGE:

    python3 ./ws852.py SUBCOMMAND

SUBCOMMANDS:

    rename      - rename all raw voicefiles in device to show timestamp
    upload      - move all renamed files to ${WS852_UPLOAD_DIR} (if well defined) [unimplemented]

RESTRICIONS:

    This must be called from within the script's directory by the
    relative path [./ws852.py] and this directory must be in the
    root directory of the device.

NOTES FOR 'rename' SUBCOMMAND:

    Renaming is in situ.

    Voice files created natively by the device match this pattern:
        "{ROOT}/FOLDER_{ch}/{nnnnnn}_{nnnn}.MP3"
    where
        {ROOT}   : the root folder of the device
        {ch}     : any character from 'ABCDE'
        {nnnnnn} : a six digit numeric string showing YYMMDD
        {nnnn}   : a four digit numeric string showing an incrementing serial number.

    All such files (and only such files) will be renamed to:
        "{ROOT}/FOLDER_{ch}/{timestamp}.ws852.mp3"
    where
        {timestamp} is a 'yyyymmddThhmmss' iso timestamp.

    The timestamp may reflect the time the voice recording began or the time the
    voice recording ended. There is no guarantee of which of these times will be
    used. Be careful interpreting the timestamp with very long recordings.

"""


# ROOT should be the root folder of the device
ROOT    = Path(os.getcwd()).parent

# FOLDERS is a list of the five folders in which voicefiles are stored.
FOLDERS = [ ROOT/('RECORDER/FOLDER_%s' % ch ) for ch in 'ABCDE']

def main():
    command=(sys.argv + [''])[1]
    if command == 'rename':
        cmd_rename()
    else:
        print(USAGE)


def cmd_rename():
    if not FOLDERS[0].is_dir(): 
        exit("This repo must be in the root of the device")
    for folder in FOLDERS:
        for path in folder.iterdir():
            rename(path)

def rename( path ):
    fname=str(path)
    if is_raw_voicefile(path):
        ts = os.path.getmtime(fname)
        dt = datetime.datetime.fromtimestamp(ts)
        timestamp = dt.strftime('%Y%m%dT%H%M%S')
        newname = '%s.ws852.mp3' % timestamp
        newpath = path.parent/newname
        print('rename: %s -> %s' % (path,newpath))
        path.rename(newpath)
    else:
        print('skip: %s' % path)



def is_raw_voicefile(path):
    def alldigits(str):
        if not str: return True
        if not str[0] in '0123456789': return False
        return alldigits(str[1:])
    name=path.name
    return ( True
        and alldigits(name[0:6])
        and name[6]=='_'
        and alldigits(name[7:11])
        and name[11:]=='.MP3'
    )

def do_folder(folder):
    for path in folder.iterdir():
        if is_raw_voicefile(path):
           rename( path )
        else:
            print( 'skipping', path )
    #for path in filter(is_raw_voicefile, folder.iterdir()):
    #    print(path)
main()
