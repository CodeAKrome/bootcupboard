#!bash
for i in {0..7}
do
    find /Volumes/photo/dpi1200/small1MB/"$i" -name '*.jpg' | python Img2Objects.py > "objects$i.tsv"
done
