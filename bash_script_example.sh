#!/bin/bash

shuffle() {
   local i tmp size max rand

   # $RANDOM % (i+1) is biased because of the limited range of $RANDOM
   # Compensate by using a range which is a multiple of the array size.
   size=${#array[*]}
   max=$(( 32768 / size * size ))

   for ((i=size-1; i>0; i--)); do
      while (( (rand=$RANDOM) >= max )); do :; done
      rand=$(( rand % (i+1) ))
      tmp=${array[i]} array[i]=${array[rand]} array[rand]=$tmp
   done
}

spotifyCreator=/Users/pilo/Developement/Programs/SpotifyOrganizer/playlist_creator.py
username=pilobasualdo
logFile=/Users/pilo/Developement/Programs/SpotifyOrganizer/Logs/creator_log.txt

echo "Starting"

## declare an array variable
declare -a array=(
                spotify:user:11134160748:playlist:7GEUpnCYxkwgPy2a3NPvCc
                spotify:user:11134160748:playlist:6zOsBtVrdl77hcBcCQZG2e
                spotify:user:11134160748:playlist:5Xirttm3pXHQsqnbUzSOs5
                spotify:user:11134160748:playlist:33OsonAwyOWTEbr0Uye04A
                spotify:user:11134160748:playlist:0U69vPSe6EJxSo0nrXQeS2
                )

shuffle

## now loop through the above array
for i in "${array[@]}"
do
    echo "Processing playlist: $i"
    python $spotifyCreator $username $i >> $logFile

done

echo "Fin"
