A utility for the Olympus WS-852 voice recorder.

OVERVIEW:
=========
This utility remames all voice files recorded on this device to reflect their creation time and the device that created them.
- old name: [{ROOT}/RECORDER/FOLDER_{X}/{YY}{MM}{DD}_{NNNN}.MP3]
- new name: [{REPO}/__RAW__/{YYYY}{MM}{DD}T{HH}{mm}{SS}.ws852.mp3]

where
- {ROOT} is the root folder of the device
- {REPO} is the root folder of the repo
- {X} is a letter in the five letter range [A..E]
- {YYYY},{YY},{MM},{DD},{HH},{mm},{SS} are the usual timestamp values
- {NNNN} is a four digit serial number

INSTALLATION:
=============

To install, simply clone the repo to the root folder of the device.

USAGE:
=====

Simply invoke the script "./process.sh" without parameters. It may be invoked by absolute or relative pathname from any directory.
