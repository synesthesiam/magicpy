#/bin/bash
PREFIX=snapshot_
EXT=png
PROCS=4

# Use glmagic.py to make all of the depth maps
echo "Generating depth maps..."
python glmagic.py -p $PREFIX -e $EXT

# Convert each depth map into a stereogram with magicpy.py (in parallel with xargs)
echo "Converting depth maps to stereograms ($PROCS threads)..."
ls -1 $PREFIX*.$EXT | xargs -I {} -n1 -P$PROCS python magicpy.py {} -o magic-{}

# Use ImageMagick to roll up all of the stereograms into an animated GIF
echo "Generating animated GIF..."
convert -delay 20 -loop 0 magic-$PREFIX*.$EXT movie.gif

# Get rid of the depth maps and stereogram frames
echo "Deleting frames"
rm $PREFIX*.$EXT
rm magic-$PREFIX*.$EXT
