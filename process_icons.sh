#!/bin/bash

# Process AWS icons mapping CSV file
# Convert SVG icons to PNG format for the diagrams library

csv_file="aws_icons_mapping.csv"

if [ ! -f "$csv_file" ]; then
    echo "Error: $csv_file not found"
    exit 1
fi

while IFS=',' read -r col1 col2 col3 col4; do
    # Remove carriage returns from Windows line endings
    col4="${col4%$'\r'}"
    # Skip empty lines
    [ -z "$col1" ] && continue
    
    # Skip NOT_FOUND entries
    [ "$col4" = "NOT_FOUND" ] && continue
    
    # Build output filename: resources/col1/col3
    col1_path="${col1//.//}"
    outfile="resources/${col1_path}/${col3}"
    infile="assets/${col4}"
    
    # Create directory if it doesn't exist
    mkdir -p "$(dirname "$outfile")"
    
    # Check if output file already exists
    if [ ! -f "$outfile" ]; then
        echo "Converting: $infile -> $outfile"
        rsvg-convert -w 256 -h 256 "$infile" -o "$outfile"
    else
        echo "Skipping: $outfile (already exists)"
    fi
    
done < "$csv_file"

echo "Icon processing complete"