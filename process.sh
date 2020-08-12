HERE=$(dirname $0)
ROOT=$(dirname $HERE)
PATTERN='/RECORDER/FOLDER_[A-F]/[0-9]*_[0-9]*.[Mm][Pp][3]'

mkdir -p $HERE/__RAW__

for oldpath in $(find $ROOT | grep ${PATTERN}); do
    newpath=$HERE/__RAW__/$(python $HERE/rename.py $oldpath)
    echo $oldpath '-->' $newpath
    mv $oldpath $newpath
done
