#!/bin/bash
if [ ! -f schema.json ]; then
    echo "schema.json is missing"
    exit 1
fi

if [ ! -f data.json ]; then
    echo "data.json is missing"
    exit 1 
fi

echo "Required files are present"