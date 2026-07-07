#!/bin/bash

if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
    echo "Usage: $0 <sport_path> <cycle_id> <end_week> [start_week (default 1)]"
    exit 1
fi

sport="$1"
cycle="$2"
end_week="$3"
start_week="${4:-1}"

if [ "$start_week" -gt "$end_week" ]; then
    temp="$start_week"
    start_week="$end_week"
    end_week="$temp"
fi

mkdir -p "$sport" || { echo "Error: Unable to create directory $sport"; exit 1; }

for week in $(seq "$start_week" "$end_week"); do
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
