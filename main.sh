#!/bin/bash

# python3 main.py

args=("$@")

# clear

DNI=${args[0]}
STEPS=${args[1]}

# echo STEPS:
# read STEPS

status=1

while [[ $status -eq 1 ]]; do
   randomCode="$(python3 main.py)"
   kitty +kitten icat --scale-up captcha.png
   captchaValue="$(python3 testOCR.py $STEPS)"
   status=$?
   echo $captchaValue
   if [[ $status -eq 1 ]]; then
      continue
   fi
   echo $randomCode
   python3 getData.py $randomCode $captchaValue $DNI
   status=$?
done
