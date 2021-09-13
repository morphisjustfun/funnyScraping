#!/bin/bash

args=("$@")

clear

# echo STEPS:
# read STEPS

arrTimes=()

for i in {0..5..1}
   do
      start=`date +%s`
      ./main.sh 71563661 5
      end=`date +%s`
      runtime=$((end-start))
      arrTimes=(${arrTimes[@]} $runtime)
   done

echo
echo TEST RESULTS

for value in "${arrTimes[@]}"
do
     echo $value
done
