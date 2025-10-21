#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <sport_path> <cycle_id>"
    exit 1
fi

sport="$1"
cycle="$2"

mkdir -p "$sport" || { echo "Error: Unable to create directory $sport"; exit 1; }

for week in {1..4}; do
    jsonFilename="${sport}/c${cycle}.s${week}.json"
    for day in {1..3}; do
        htmlFilename="${sport}/c${cycle}.s${week}.d${day}.html"
        if [ ! -f "$htmlFilename" ]; then
            touch "$htmlFilename"
            echo "Created: $htmlFilename"
        else
            echo "Already exists: $htmlFilename (not overwritten)"
        fi
    done
    if [ ! -f "$jsonFilename" ]; then
        touch "$jsonFilename"
        echo "Created: $jsonFilename"
    else
        echo "Already exists: $jsonFilename (not overwritten)"
    fi
done

echo "Processing complete."
