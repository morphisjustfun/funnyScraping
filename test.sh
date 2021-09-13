#!/bin/bash

declare -A arr

for i in $(seq 50 1 100); do 
   # convert captcha.png -colorspace Gray -blur 0 -level 0,$i% test1.jpg
   convert CROP-2.jpg -colorspace Gray -blur 0 -level 0,$i% test1.jpg
   kitty +kitten icat test1.jpg
   value=$(tesseract -c tessedit_char_whitelist=0123456789 --psm 7 test1.jpg -)
   value=`echo $value | tr -dc '0-9'`
   echo $value
   if [[ -z "$value" ]]; then
      echo Empty
   else
      if [[ -z "${arr[${value}]}" ]]; then
         arr["$value"]=1
      else
         newValue=$((${arr[${value}]}+1))
         arr["$value"]=newValue
      fi
   fi
   done

echo Print array
echo 

for key in ${!arr[@]}; do
   val=$((${arr[${key}]}))
   echo $key $val
 done
