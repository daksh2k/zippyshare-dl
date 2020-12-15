#!/bin/bash
echo "Enter the name or path of the file:"
read input
while IFS= read -r line || [ -n "$line" ];
do
   if [ -z "$line" ]
   then
        echo"Empty line moving to next..."
        continue
   else
   xdg-open $line
   echo "Opened $line"
   fi
 done<"$input"
