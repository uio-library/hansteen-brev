#!/usr/bin/env bash

count=0
total=$(ls -1q files/*.tif | wc -l)
start=`date +%s`

for filename in files/*.tif; do
  basename="${filename%.*}"
  MAGICK_TEMPORARY_PATH=/www/htdocs/tmp convert -format jpg -thumbnail 250x250 -unsharp 0x.5 "$filename" "${basename}_thumb.jpg"
  cur=`date +%s`
  count=$(( $count + 1 ))
  pd=$(( $count * 73 / $total ))
  runtime=$(( $cur-$start ))
  estremain=$(( ($runtime * $total / $count)-$runtime ))
  printf "\r%d.%d%% complete ($count of $total) - est %d:%0.2d remaining\e[K" $(( $count*100/$total )) $(( ($count*1000/$total)%10)) $(( $estremain/60 )) $(( $estremain%60 ))
done

printf "\ndone\n"
