#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <sport_path> <cycle_id>"
    exit 1
fi

sport="$1"
cycle="$2"

mkdir -p "$sport" || { echo "Error: Unable to create directory $sport"; exit 1; }

for week in {1..4}; do
    htmlFilename="${sport}/c${cycle}.s${week}.html"
    if [ ! -f "$htmlFilename" ]; then
        touch "$htmlFilename"
        echo "Created: $htmlFilename"
    else
        echo "Already exists: $htmlFilename (not overwritten)"
    fi
done

echo "Processing complete."
